'''

Create datacard for Higgs Combine Tool

python createCard.py [card config file]

ex) python createCard.py ./config/card.config

'''

from ROOT import *
import os, sys

class Card:
    '''
    Datacard for Higgs Combined Tool
    '''    

    def __init__(self, binIndex, configFile='./config/card.config'):
        self.configFile = configFile
        self.binIndex = binIndex

        self.description = '# VBF SUSY temp'
       
        self.iChannel = 'imax 1 number of channels'
        self.jBkg = 'jmax '
        self.kSysSource = 'kmax * number of nuisance parameters (sources of systematic uncertainties)'
        
        self.label = '# we have just one channel for now'
        self.channelLabel = 'bin channel'
        self.obs = 'observation '

        self.channelInfo = 'bin '
        self.processName = 'process '
        self.processIndex = 'process '
        self.rate = 'rate '

        self.integrals = []
        self.nBins = 0
 
        self.processes = []
        self.nSig = 0
        self.nBkg = 0
        self.systematics = []

        self.lines = []
        self.card = ''

        self.outDir = './cards/'
        self.outName = 'Datacard'
      
        self.initializeCard() 

    def getConfigs(self): 
        f = open(self.configFile, 'r')
        lines = [line[:-1] for line in f if (len(line[:-1]) != 0 and '//' not in line)]
 
        self.systematics = []

        for idx, line in enumerate(lines):
            # Output datacard name
            if ('# Name of' in line) and (not lines[idx+1].startswith('#')):
                self.outName = lines[idx+1]
            
            # Output directory
            elif '# Directory' in line:
                self.outDir = lines[idx+1]
                if not self.outDir.endswith('/'):
                    self.outDir += '/'
                os.system('mkdir -p {}'.format(self.outDir))

            # Get the list of processes and uncertainties
            elif ('## <-- Below' in line) and ('Processes') in lines[idx+1]:
                self.processes = lines[idx+1].split(' ')
                self.processes.pop()
                self.processes.remove('Processes')

                idx += 1
                while '### number of SIG' not in lines[idx+1]:
                    idx += 1
                    if 'label' in lines[idx]:
                        self.systematics.append(lines[idx].split(' ')[1]) 
                    elif 'distr' in lines[idx]:
                        self.systematics.append(lines[idx].split(' ')[1]) 
                    elif 'values' in lines[idx]:
                        value = ''
                        for i in lines[idx].split(' ')[1:]:
                            value += '{} '.format(i) 
                        self.systematics.append(value)

            # Get the number of signal and bkg processes
            elif '### number of SIG' in line:
                self.nSig = int(lines[idx+1].split(' ')[1])
                self.nBkg = int(lines[idx+2].split(' ')[1])
                self.jBkg += '{} number of bkg sources'.format(self.nBkg)

        #print('\n{} successfully read.\n'.format(self.configFile))

    def getBinYields(self, yieldsDir='./binYields/'):
        # Read from input file the bin contents for each processes
        self.integrals = []
        fileName = yieldsDir+self.processes[0]

        for i in range(self.nSig+self.nBkg):
            fileName = yieldsDir+self.processes[i]+'.txt'
        
            f = open(fileName, 'r')
            self.integrals.append([line[:-1] for line in f if (len(line[:-1]) != 0)])
            
        self.nBins = len(self.integrals[0])

    def addProcessByChannel(self):
        #self.obs += '{:<14.10f} '.format(float(self.integrals[0][self.binIndex]))
        self.obs += '0 '

        for i in range(self.nSig):
            self.channelInfo += 'channel '
            self.processName += '{} '.format(self.processes[i])
            self.processIndex += '{} '.format(i*(-1))   # signal numbering scheme: 0, -1, -2, ...
            self.rate += '{:<14.10f} '.format(float(self.integrals[i][self.binIndex]))

        for i in range(self.nSig, self.nSig+self.nBkg):
            self.channelInfo += 'channel '
            self.processName += '{} '.format(self.processes[i])
            self.processIndex += '{} '.format(i+1-self.nSig) # bkg numbering scheme: 1, 2, 3, ...
            self.rate += '{:<14.10f} '.format(float(self.integrals[i][self.binIndex]))

        self.lines.append(self.obs)
        self.lines.append('------------')            
        self.lines.append(self.channelInfo)
        self.lines.append(self.processName)
        self.lines.append(self.processIndex)
        self.lines.append(self.rate)
        self.lines.append('------------')

    def initializeCard(self):
        self.getConfigs()
        self.lines = [ self.description, self.iChannel, self.jBkg, self.kSysSource, '------------', self.label, self.channelLabel ] 
        self.getBinYields()
        self.addProcessByChannel()
        self.addSystematics()
        for line in self.lines:
            self.card += line+'\n' 

    def printCard(self):
        print(self.card)

    def saveCardAsTxt(self):
        outFileName = '{}/{}_bin{}.txt'.format(self.outDir, self.outName, self.binIndex) 
        os.system('mkdir -p {}'.format(self.outDir))
        if os.path.isfile(outFileName):
            os.remove(outFileName)
            print('{} exits. deleting it..'.format(outFileName))
        outFile = open(outFileName,'a')
        outFile.write(self.card)
        outFile.close()
        print('Saved: {}'.format(outFileName))

    def addSystematics(self):
        nSys = len(self.systematics)/3
        
        for sys in range(nSys):
            sys *= 3
            line = '{} {} {}'.format(self.systematics[sys], self.systematics[sys+1], self.systematics[sys+2]) 
            self.lines.append(line)


card = Card(0)
nBins = card.nBins
card = card.saveCardAsTxt()

for i in range(1,nBins):
    card = Card(i)
    card.saveCardAsTxt()
