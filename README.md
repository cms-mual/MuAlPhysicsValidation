# Muon Alignment Physics Validation

**Checkout the physics validation code**
1. Follow the instructions in: https://github.com/cms-mual/Alignment/blob/CMSSW_9_2_6/README.md
2. There you will also see how to take MuAlPhysicsValidation (basically just do https://github.com/cms-mual/MuAlPhysicsValidation.git in your favorite release).

**The idea:**
1. You need to take RAWRECO SingleMuon events and reconstruct muons using the Muon Geometry and/or APEs you want to test.
2. Run the Analyzer, in order to produce Ntuples with muon and dimuon information.
3. Use the Ntuples to plot the reconstruction performance, overimposing the results obtained using several geometries and/or APEs.

**Refitting**

1. cd MuAlPhysicsValidation/MuAlRefit
2. cp -r MuAlRefit_Run2017B_RAWreco_2016Geom_01 CRAB_MYSTUDY; cd CRAB_MYSTUDY
3. Change the crab configuration file: **crab_data.py**:

    Change the requestName and outLFNDirBase 
    Change the Input dataset: inputDataset and the JSON file (if data)
    The python command you will execute: psetName
    inputFiles: inputFiles (CRAB cannot see external files if you do not specify them. If you want to use special APE, Geometries or GPR, you have to give here the path. CRAB will import them and copy them in the same place he runs cmsRun. So do not simply put the path name in the python code you will run.)

1d. One your crab file if fine, change the python code you will run. You can rename it with a better name:

    mv refit_PromptGT_TrackerMay2016_MuAl_DT2016D6DOF_CSC2016D3DOF_cfg.py refit_PromptGT_MYNAME_cfg.py
 
1e. In **refit_PromptGT_MYNAME_cfg.py** you want to customize:

    The GT.
    The JSON file.
    The APE, GPR, muon geometry and tracker geometry (all external files have to be declared in the CRAB file as inputFiles).

1f. Submit CRAB jobs:

    cmsenv
    voms-proxy-init -voms cms
    source /cvmfs/cms.cern.ch/crab3/crab.sh
    crab submit -c crab_data.py
    crab status (and all the CRAB commands to check status, resubmit etc...)

1g. Once the jobs are finished, the output will be in EOS, as spdecified by outLFNDirBase location in the crab cfg file.

---
## Analysis

2a. Change directory to MuAlAnalyzer:

    cd ../MuAlAnalyzer

2b. Create a Working directory for this comparison (it could be the folder name on EOS from the previous step)

    mkdir MuAlRefit_MYSTUDY

2c. Create a file list for the sample to be analyzed in **Create_Input.sh**; this will be the EOS folder that contains the Refit files and a python file that will create the file list. You will specify these on lines 2 and 3 of **Create_Input.sh**:

    Folder="/store/group/alca_muonalign/<user>/<crab_output_location>"
    fileTXT="MuAlRefit_MYSTUDY/MuAlRefit_MYSTUDY_list.py"

Then, execute the script.

    bash Create_Input.sh 
    cd MuAlRefit_MYSTUDY

2d. Now copy here the python file you will change to run your comparison **muAlAnalyzer_Data_cfg.py**.
      
    cp ../muAlAnalyzer_Data_cfg.py .
    cp ../createJobs.py .
    python createJobs.py $FILELIST$ $N_JOBS$
`FILELIST` is the one you created and `N_JOBS` is the job splitting you want to use; recommend `N_JOBS` ~800 jobs and to remain in the range [500-900] jobs.

2e. Now you can submit the jobs:

    source submit.sh
    
2f. hadd the output ROOT files into a single ROOT file and clean space.
 
    hadd FINALFILE.root out_*root
    rm -rf out_*root
    rm -rf LSF*

---
## Plotting

3a. Change directory to PerformancePlots:

    cd ../PerformancePlots

3b. Use **myPlot_2016E_3vs6DOF.py** as a model for a new pyhton command to make the plots

    cp myPlot_2016E_3vs6DOF.py myPlot_MINE.py

3c. You need to change:
    
    maxEntries -> for test set to low value, for final plots set to -1 (all events)
    samples -> change the path to the root files you created in the previous step
    combineHistos -> decide what samples are shown in the same plot (E.g. [0,1] to show the first and second only).

3d. Launch the command:

    python myPlot_MINE.py

## Plotting with Performance Plots 2.0
This is an alternative procedure for step 3. 

3'a. Change directory to PerformancePlots_2_0

    cd ../PerformancePlots_2_0

3'b. Point **Step1_make_2d_plots.py** at the root file you hadded in the previous step, also specifying an output file:

    python Step1_make_2d_plots.py ../MuAlAnalyzer/MuAlRefit_MYSTUDY/FINALFILE.root MuAlRefit_Step1_plots std -b
    
This will create a folder with some 2D plots in it named MuAlRefit_Step1_plots as well as a ROOT file MuAlRefit_Step1_plots.root. To make comparison plots with another analysis, you may repeat this step to create multiple root files to be used in step 3'c.

3'c. Edit **Step2_makeProfiles.py** to make comparison plots over groups of analysis datasets. You need to edit the following fields:
    
    tot_fileList
    tot_fileListName
    tot_colors
    Combinations
    tot_outputFolderName
    
Specify the list of root files created in step 3'b in `tot_fileList`, labeling each dataset in `tot_fileListName` appropriately, and assigning colors and the grouping in `tot_colors` and `Combinations`, respectively. Finally, create an output folder to store all your comparison plots in the `tot_outputFolderName` field. Then, run the code:

    python Step2_makeProfiles.py -b


## Notes:

1 Input to Refit is full RECO, not ALCARECO!
