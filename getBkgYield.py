'''

Get list of bkg root files, access histograms, rebin, and save the bin contents as output txt files for each bkg processes

Run 'python getBkgYield.py [histo config file]'

ex) python getBkgYield.py ./config/histo.config

'''

import os,sys
import numpy as np
from ROOT import *

class BinYields:
    def __init__(self,configFile='./config/histo.config'):
        if not os.path.isfile(configFile):
            print('Histogram config file "{}" does not exist. Terminating the program.'.format(configFile))
            sys.exit()

        self.configFile = configFile
        self.fileDir = 'directory where input root files are stored',

        self.signal = 'list of signal samples',
        self.bkg = 'list of background samples',
        self.data = 'list of data',

        self.kinematic = 'name or label of histogram',
        self.cutStep = 'name of the cut step after which the histogram is from',
        self.binning = 'binning of the histogram; histogram will be rebinned with this binning'

        self.getConfigs()

    def getConfigs(self): 
        f = open(self.configFile, 'r')
        lines = [line[:-1] for line in f if (len(line[:-1]) != 0 and '//' not in line)]

        self.signal = []
        self.bkg = [] 
        self.data = []
        self.binning = []

        for idx, line in enumerate(lines):
            # Get root file directory
            if '# Input file directory' in line:
                self.fileDir = lines[idx+1]
                if not self.fileDir.endswith('/'):
                    self.fileDir += '/'
            # Get the list of samples
            elif ('# SIG' in line) or ('# BKG' in line) or ('# DATA' in line):
                if '# SIG' in line:
                    while '# BKG' not in lines[idx+1]:
                        idx += 1   
                        self.signal.append(lines[idx][:-5])
                elif '# BKG' in line:
                    while '# DATA' not in lines[idx+1]:
                        idx += 1
                        self.bkg.append(lines[idx][:-5])
                elif '# DATA' in line:
                    while '[2] Histo' not in lines[idx+1]:
                        idx += 1
                        self.data.append(lines[idx][:-5])
            # Get the histogram information
            elif '# Name of the histo' in line:
                self.kinematic = lines[idx+1]
            elif '# Name of the cut' in line:
                self.cutStep = lines[idx+1]
            elif '# Binning' in line:
                self.binning = np.array([float(bins) for bins in lines[idx+1].replace(' ','').split(',')])
                self.nBins = self.binning.size -1

        print('\n{} successfully read.\n'.format(self.configFile))

    def saveBinYields(self, process, outDir='./binYields/'):
        if not outDir.endswith('/'):
            outDir += '/'

        if not os.path.isdir(outDir):
            os.system('mkdir {}'.format(outDir))
            print('\nCreated: {}'.format(outDir))

        # get histogram and rebin
        f = TFile('{}{}.root'.format(self.fileDir, process))

        hRead = f.Get('{}/{}'.format(self.cutStep, self.kinematic))
        hNew = hRead.Rebin(self.nBins, '{} histo rebinned'.format(process), self.binning)

        # save bin contents as a txt file
        outFileName = '{}{}.txt'.format(outDir,process)
        if os.path.isfile(outFileName):
            os.remove(outFileName)
            print('{} exits. deleting it..'.format(outFileName))
        outFile = open(outFileName, 'a')
        for i in range(1, self.nBins+1):
            #outFile.write('{} {}\n'.format(i, hNew.GetBinContent(i)))
            outFile.write('{}\n'.format(hNew.GetBinContent(i)))
        print('Saved: {}\n'.format(outFileName))

    def saveCardConfig(self,outDir='./config/', sampleConfig='./config/card_format.config'):
        outFileName = '{}card.config'.format(outDir)
        try:
            os.system('cp {} {}'.format(sampleConfig,outFileName))
        except:
            print('Cannot copy config format from {}. Terminating the program.'.format(sampleConfig))
            sys.exit(1)

        f = open(outFileName,"a")
        lines = [ 'Processes ', '### number of SIG and BKG processes (do NOT change below)\n' ]

        for signal in self.signal:
            lines[0] += '{} '.format(signal)
        for bkg in self.bkg:
            lines[0] += '{} '.format(bkg)
        f.write(lines[0])
        f.write('\n\n\n')

        lines[1] += 'nSig {}\nnBkg {}'.format(len(self.signal), len(self.bkg))
        f.write(lines[1])
        
        f.close()       
 
        print('Created: {}\n'.format(outFileName))


bins = BinYields()

for signal in bins.signal:
    bins.saveBinYields(signal)

for bkg in bins.bkg:
    bins.saveBinYields(bkg)

for data in bins.data:
    bins.saveBinYields(data)

bins.saveCardConfig()
