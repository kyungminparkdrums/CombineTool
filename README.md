## Create Datacard for Higgs Combine Tool

[Resources on preparing the datacard (from the official Combine Tool website)](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part2/settinguptheanalysis.html)

**Step 1. Get .txt files for histogram bin contents for each processes**
```
python getBkgYield.py [histogram config file]

ex) python getBkgYield.py ./config/histo.config
```

**Step 2. Create datacards based on txt files from Step 1**
```
python createCard.py [card config file]

ex) python createCard.py ./config/card.config
```

**Step 2. Combine the datacards (for each histogram bins) from Step 2 as one datacard**

In `$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/scripts`, run the command below to get a datacard that combines all datacards from Step 3.
```
python combineCards.py [/path to cards created from Step 2/*] > [output card name]

ex) python combineCards.py ./cards/* > $CMSSW_BASE/src/CombineTool/VBF_card.txt
```

## Run Higgs Combine Tool: Calculate Significance
**Run with toy model data**

In `$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/`, run the command below
```
combine -M Significance [datacard from above] -t -1 --expectSignal=1

ex) combine -M Significance $CMSSW_BASE/src/CombineTool/VBF_card.txt -t -1 --expectSignal=1
``` 
