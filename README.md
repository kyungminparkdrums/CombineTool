## Create Datacard for Higgs Combine Tool

[Resources on preparing the datacard (from the official Combine Tool website)](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part2/settinguptheanalysis.html)

**Step 1. Edit `./config/histo.config` as necessary**

From the sample `histo.config` file in the code block below, change the following:
- Under *# Input file directory*: directory where the root files are stored.
- Under *# Name of the input root files in the directory above*: name of the root files, i.e. ZJetsToNuNu.root, under *## SIGNAL sample(s)*, *## BKG sample(s)*, and/or *## DATA*, for signal, background, and data samples, respectively. 
- Under *# Name of the histogram stored in the root files*: i.e. LargestDiJetMass
- Under *# Name of the cut step after which you want the histogram from*: i.e. NRecoBJet
- Under *# Binning of the histogram from the left end to the right end values: histogram will be rebinned with this binning*: i.e. 1000, 1500, 2000, 2500, 3000, 3500, 4000 

```
// This is an input config file for `getBkgYield.py`
// Fill out the sections [1] and [2] below in this config file
// To comment out any line(s), use // at the beginning of the line(s)
// Do NOT change any comment lines starting with #
// For more information, check README


### [1] Input ROOT files (after Analyzer&Plotter)

# Input file directory
/home/kyungminpark/CMSSW_10_2_18/src/Forked/Plotter/2016/2016_SR/

# Name of the input root files in the directory above
## SIGNAL sample(s)
VBF-EWKino_Higgsino_M100_dM10.root

## BKG sample(s)
ZJetsToNuNu.root
WJetsToLNu.root
EWK_Z.root
EWK_W.root

## DATA (optional if running with toy model)
// HTMHT_Run2016.root



### [2] Histogram Information

# Name of the histogram stored in the root files
LargestDiJetMass

# Name of the cut step after which you want the histogram from
NRecoBJet

# Binning of the histogram from the left end to the right end values: histogram will be rebinned with this binning
1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4500, 5000

```

**Step 2. Run `getBkgYields.py` to get .txt files for histogram bin contents for each processes**

Run the command below, then `./binYields/` and `./config/card.config` will be created.
- `./binYields/`: stores the yields for each bin, for each processes
- `./config/card.config`: config file to run the `createCard.py` script later. Add some of datacard output settings and add systematics here.

```
python getBkgYield.py [histogram config file from Step 1]

ex) python getBkgYield.py ./config/histo.config
```

**Step 3. Edit `./config/card.config` as necessary**


**Step 4. Create datacards for each histogram bins**

Run the command below, then the Higgs Combine Tool datacards for each histogram bins will be created.
```
python createCard.py [card config file]

ex) python createCard.py ./config/card.config
```

**Step 5. Combine the datacards (for each histogram bins) from Step 4 as one datacard**

In `$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/scripts`, run the command below to get a datacard that combines all datacards from Step 4.
```
python combineCards.py [/path to cards created from Step 4/*] > [output card name]

ex) python combineCards.py ./cards/* > $CMSSW_BASE/src/CombineTool/VBF_card.txt
```

## Run Higgs Combine Tool: Calculate Significance
**Run with toy model data**

In `$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/`, run the command below
```
combine -M Significance [datacard from above] -t -1 --expectSignal=1

ex) combine -M Significance $CMSSW_BASE/src/CombineTool/VBF_card.txt -t -1 --expectSignal=1
``` 
