import FWCore.ParameterSet.Config as cms 
import os

process = cms.Process("MUALREFIT")
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('file:CCE41E3E-C38F-E811-A8E0-FA163E23AFD1.root')
    fileNames = cms.untracked.vstring(
        'file:./D6EF7545-BA2E-034C-A995-C3F54077BF73.root'
      #'file:/afs/cern.ch/work/r/rymuelle/public/MA_optimizer/CMSSW_10_5_0/src/MuAlPhysicsValidation/MuAlRefit/CRAB_MC_Zmumu_ideal/ZMM_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGI_L1_DIGI2RAW_L1Reco_RECO_inRECO.root'
      )
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(20))

process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring("cout"),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR"),
                                                              ERROR = cms.untracked.PSet( limit = cms.untracked.int32(10) )
                                                             )
                                   )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "106X_dataRun2_v28" #! GT Here

process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load("Geometry.CMSCommonData.cmsExtendedGeometry2018XML_cfi")
process.load('Configuration.StandardSequences.MagneticField_cff')

process.load("Configuration.StandardSequences.Reconstruction_cff")
#process.load("Configuration.StandardSequences.ReconstructionCosmics_cff")
#process.load("RecoTracker.TrackProducer.TrackRefitter_cfi")
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
#process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")

#process.MeasurementTrackerEvent = process.MeasurementTrackerEvent.clone()

process.muAlGeneralCosmicTracks = process.TrackRefitterP5.clone()
process.muAlGeneralCosmicTracks.src = 'muons1Leg'
process.muAlGeneralCosmicTracks.TrajectoryInEvent = True



process.Path = cms.Path(process.muAlGeneralCosmicTracks)

process.out = cms.OutputModule("PoolOutputModule",
                                outputCommands = cms.untracked.vstring("keep *",
                                                                       "keep GenEventInfoProduct_generator_*_*",
                                                                       "keep edmHepMCProduct_generator_*_*",
                                                                       "keep *_genParticles_*_*",
                                                                       "keep recoBeamSpot_offlineBeamSpot_*_*",
                                                                       "keep *_TriggerResults_*_*",
                                                                       "keep recoMuons_*_*_MUALREFIT",
                                                                       "keep recoTracks_*_*_MUALREFIT",
                                                                       "keep recoTrackExtras_*_*_MUALREFIT"
                                                                       ),
                                fileName = cms.untracked.string("output.root"),
                                SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("Path")),
                                )

process.EndPath = cms.EndPath(process.out)
