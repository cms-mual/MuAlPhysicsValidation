import FWCore.ParameterSet.Config as cms 
import os

ijob = int(os.environ["IJOB"])
input_files = os.environ["INPUTFILES"].split(" ")

process = cms.Process("MUALREFIT")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(*input_files)
)

import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274240_13TeV_PromptReco_Collisions16_JSON_MuonPhys.txt').getVLuminosityBlockRange()


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring("cout"),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR"),
                                                              ERROR = cms.untracked.PSet( limit = cms.untracked.int32(10) )
                                                             )
                                   )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "80X_dataRun2_Prompt_v8" # Prompt GT for 2016B data

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
#process.load("Configuration.Geometry.GeometryExtended2016Reco_cff")   # this geometry leads to _wrong_ results of alignment
process.load("Geometry.CMSCommonData.cmsExtendedGeometry2016aXML_cfi") # is this correct geometry for 2016 run???
process.load('Configuration.StandardSequences.MagneticField_cff')

process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("RecoTracker.TrackProducer.TrackRefitter_cfi")
process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")

process.MeasurementTrackerEvent = process.MeasurementTrackerEvent.clone()

process.muAlGeneralTracks = process.TrackRefitter.clone()

process.muAlAncientMuonSeed = process.ancientMuonSeed.clone()

process.muAlStandAloneMuons = process.standAloneMuons.clone()
# this line switch on "old" hit based muon reconstruction
#process.muAlStandAloneMuons.STATrajBuilderParameters.BWFilterParameters.MuonTrajectoryUpdatorParameters.Granularity = 2
process.muAlStandAloneMuons.InputObjects = cms.InputTag("muAlAncientMuonSeed")

process.muAlGlobalMuons = process.globalMuons.clone()
process.muAlGlobalMuons.TrackerCollectionLabel = cms.InputTag("muAlGeneralTracks")
process.muAlGlobalMuons.MuonCollectionLabel = cms.InputTag("muAlStandAloneMuons","UpdatedAtVtx")

process.muAlTevMuons = process.tevMuons.clone()
process.muAlTevMuons.MuonCollectionLabel = cms.InputTag("muAlGlobalMuons")

process.muAlGlbTrackQual = process.glbTrackQual.clone()
process.muAlGlbTrackQual.InputCollection = cms.InputTag("muAlGlobalMuons")
process.muAlGlbTrackQual.InputLinksCollection = cms.InputTag("muAlGlobalMuons")

process.muAlMuons = process.muons1stStep.clone()
process.muAlMuons.inputCollectionTypes = cms.vstring('inner tracks','links','outer tracks','tev firstHit','tev picky','tev dyt')
process.muAlMuons.inputCollectionLabels = cms.VInputTag( cms.InputTag("muAlGeneralTracks"),
                                                         cms.InputTag("muAlGlobalMuons"),
                                                         cms.InputTag("muAlStandAloneMuons","UpdatedAtVtx"),
                                                         cms.InputTag("muAlTevMuons","firstHit"),
                                                         cms.InputTag("muAlTevMuons","picky"),
                                                         cms.InputTag("muAlTevMuons","dyt")
                                                       )

process.muAlMuons.fillGlobalTrackQuality = cms.bool(True)
process.muAlMuons.globalTrackQualityInputTag = cms.InputTag('muAlGlbTrackQual')
#process.muAlMuons.fillGlobalTrackRefits = cms.bool(False)

# This is to load new CondDB
from CondCore.DBCommon.CondDBSetup_cfi import *
#from CondCore.CondDB.CondDB_cfi import *

# New Tracker geometry released in May 2016
process.GlobalTag.toGet = cms.VPSet(
        ###### starts customization of tracker part
         cms.PSet(record = cms.string("TrackerAlignmentRcd"),
                  tag =  cms.string("TrackerAlignment_MP_Run2016B_v2"),
                  connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                  ),
         cms.PSet(record = cms.string("TrackerAlignmentErrorExtendedRcd"),
                  tag =  cms.string("TrackerAlignmentExtendedErrors_MP_Run2016B"),
                  connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                  ),
         cms.PSet(record = cms.string("SiPixelTemplateDBObjectRcd"),
                  tag =  cms.string("SiPixelTemplateDBObject_38T_2016_v1_hltvalidation"),
                  connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                  )
)

# Muon geometry
process.muonDtAlignment = cms.ESSource("PoolDBESSource", CondDBSetup,
                                     connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONALIGN/www/muonGeometries/2016-05_data_FirstAlignmentWithRun2016B/data_DT-1100-110001_SingleMuon_Run2016B-PromptReco_MuAlCalIsolatedMu-v3_RECO_8_0_8_pt20_LatestCond2_03.db'),
                                     toGet   = cms.VPSet(cms.PSet(record = cms.string("DTAlignmentRcd"),  tag = cms.string("DTAlignmentRcd")))
                                     )
process.es_prefer_muonDtAlignment = cms.ESPrefer("PoolDBESSource","muonDtAlignment")

process.muonCscAlignment = cms.ESSource("PoolDBESSource", CondDBSetup,
                                     connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONALIGN/www/muonGeometries/2016-05_data_FirstAlignmentWithRun2016B/data_CSC-1100-100001_SingleMuon_Run2016B-PromptReco_MuAlCalIsolatedMu-v3_RECO_8_0_8_pt20_LatestCond2_Shifted_03.db'),
                                     toGet   = cms.VPSet(cms.PSet(record = cms.string("CSCAlignmentRcd"), tag = cms.string("CSCAlignmentRcd")))
                                     )
process.es_prefer_muonCscAlignment = cms.ESPrefer("PoolDBESSource","muonCscAlignment")

process.globalPosition = cms.ESSource("PoolDBESSource", CondDBSetup,
                                     connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONALIGN/www/muonGeometries/2016-05_data_FirstAlignmentWithRun2016B/GPR_May24_2016_SW808_gprGT_Tk_MP_Run2016B_v2_dL4_iter1.db'),
                                     toGet   = cms.VPSet(cms.PSet(record = cms.string("GlobalPositionRcd"), tag = cms.string("IdealGeometry")))
                                     )
process.es_prefer_globalPosition = cms.ESPrefer("PoolDBESSource","globalPosition")

# Asymptotic Muon APEs
process.GlobalTag.toGet = cms.VPSet(
         cms.PSet(record = cms.string("CSCAlignmentErrorExtendedRcd"),
                  tag =  cms.string("MuonCSCAPEObjectsExtended_v0_mc"),
                  connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                  ),
         cms.PSet(record = cms.string("DTAlignmentErrorExtendedRcd"),
                  tag =  cms.string("MuonDTAPEObjectsExtended_v0_mc"),
                  connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                  )
)


process.Path = cms.Path(process.MeasurementTrackerEvent * process.muAlGeneralTracks * process.muAlAncientMuonSeed * process.muAlStandAloneMuons * process.muAlGlobalMuons * process.muAlTevMuons * process.muAlGlbTrackQual * process.muAlMuons)

process.out = cms.OutputModule("PoolOutputModule",
                                outputCommands = cms.untracked.vstring("drop *",
                                                                       "keep GenEventInfoProduct_generator_*_*",
                                                                       "keep edmHepMCProduct_generator_*_*",
                                                                       "keep *_genParticles_*_*",
                                                                       "keep recoBeamSpot_offlineBeamSpot_*_*",
                                                                       "keep *_TriggerResults_*_*",
                                                                       "keep recoMuons_*_*_MUALREFIT",
                                                                       "keep recoTracks_*_*_MUALREFIT",
                                                                       "keep recoTrackExtras_*_*_MUALREFIT"
                                                                       ),
                                fileName = cms.untracked.string("output_%03d.root" % ijob),
                                SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("Path")),
                                )

process.EndPath = cms.EndPath(process.out)
