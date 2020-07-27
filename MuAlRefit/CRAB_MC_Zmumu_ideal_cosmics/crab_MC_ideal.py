from CRABClient.UserUtilities import config
config = config()

config.section_("General")
config.General.requestName = 'MuAlRefit_MC_Zmumu_01'
config.General.workArea = 'crab_projects'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'refit_ideal_MuAl_cfg.py'
config.JobType.outputFiles = ['output.root']
#6DOF
config.JobType.inputFiles = ['Geometries/muonGeometry_IDEAL_AllZeroes.Ape6x6.StdTags.746p3.DBv2.db','Geometries/inertGlobalPositionRcd.StdTags.746p3.DBv2.db']

config.section_("Data")
config.Data.inputDataset = '/Zmumu_ideal_M50_Pythia8_13TeV/lpernie-crab_Zmumu_ideal_RECO_01-065fca95412c9afd9f37bf4c5781bbb0/USER'
config.Data.inputDBS = 'phys03' # global`
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outLFNDirBase =  '/store/group/alca_muonalign/lpernie/MuAlRefit_MC_Zmumu_01'
config.Data.publication = False

config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'
