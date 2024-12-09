// -*- C++ -*-
//
// Package:    MuAlAnalyzer
// Class:      MuAlAnalyzer
// 
/**\class MuAlAnalyzer MuAlAnalyzer.cc Analyzers/MuAlAnalyzer/src/MuAlAnalyzer.cc

Description: [one line class summary]

Implementation:
[Notes on implementation]
 */
//
// Original Author:  Yuriy Pakhotin
//         Created:  Fri Nov  8 01:13:03 CST 2013
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"


#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TRandom.h"

//
// class declaration
//

class MuAlAnalyzer : public edm::one::EDAnalyzer<> {
  public:
    explicit MuAlAnalyzer(const edm::ParameterSet&);
    ~MuAlAnalyzer();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginJob() ;
    virtual void analyze(const edm::Event&, const edm::EventSetup&);
    virtual void endJob() ;
    virtual void beginRun(edm::Run const&, edm::EventSetup const&);
    virtual void endRun(edm::Run const&, edm::EventSetup const&);
    virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
    virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

    //--------------------------- member data ---------------------------

    Int_t m_debugLevel;
    edm::InputTag m_recoMuons;    // Label to access reconstructed muons
    edm::InputTag m_genParticles; // Label to access generator particles
    edm::InputTag m_recoBeamSpot;

    edm::EDGetTokenT<reco::MuonCollection> recoMuonCollectionToken_;
    edm::EDGetTokenT<reco::BeamSpot> recoBeamSpotToken_;
    edm::EDGetTokenT<reco::GenParticleCollection> recoGenParticleToken_;

    edm::EDGetTokenT<edm::TriggerResults> m_trigRes;

    bool  m_fillGenMuons;
    Int_t m_genMuonMotherId;
    bool  m_fillRecoMuons;
    bool  m_fillRecoDimuons;

    TTree * m_tree_info;
    TTree * m_tree_events;
    Int_t b_n_recoMuons;
    Int_t b_n_genMuons;
    Int_t b_n_recoDimuons;

    std::vector<std::string> signalHltPaths_;

    // HLT
    bool b_HLT_0;
    bool b_HLT_1;
    bool b_HLT_2;

    // GEN muons
    TTree * m_tree_genMuons;
    Int_t   b_genMu_q;
    Int_t   b_genMu_motherId;
    Float_t b_genMu_pt;
    Float_t b_genMu_eta;
    Float_t b_genMu_phi;

    // RECO muons
    TTree * m_tree_recoMuons;
    Int_t b_recoMu_q; // muon charge
    Int_t b_recoMu_IsoPF04; // muon charge

    // GLB muons
    Bool_t  b_recoMu_glb;
    Float_t b_recoMu_glb_pt;
    Float_t b_recoMu_glb_eta;
    Float_t b_recoMu_glb_phi;
    Float_t b_recoMu_glb_phi_error;
    Float_t b_recoMu_glb_nchi2;
    Float_t b_recoMu_glb_chi2;
    Float_t b_recoMu_glb_pterror;
    Float_t b_recoMu_glb_qoverpterror;
    Int_t   b_recoMu_glb_nhits;

    // GEN muons matched to GLB muons
    Bool_t  b_recoMu_glb_gen;
    Int_t   b_recoMu_glb_gen_motherId;
    Float_t b_recoMu_glb_gen_dR;
    Float_t b_recoMu_glb_gen_pt;
    Float_t b_recoMu_glb_gen_eta;
    Float_t b_recoMu_glb_gen_phi;

    // inner tracks of GLB muons
    Float_t b_recoMu_glb_trk_pt;
    Float_t b_recoMu_glb_trk_eta;
    Float_t b_recoMu_glb_trk_phi;

    // "picky" tracks of GLB muons
    Bool_t  b_recoMu_glb_pic;
    Float_t b_recoMu_glb_pic_pt;
    Float_t b_recoMu_glb_pic_eta;
    Float_t b_recoMu_glb_pic_phi;

    // STA muons
    Bool_t  b_recoMu_sta;
    Float_t b_recoMu_sta_pt;
    Float_t b_recoMu_sta_eta;
    Float_t b_recoMu_sta_phi;
    Float_t b_recoMu_sta_nchi2;
    Float_t b_recoMu_sta_chi2;

    Float_t b_recoMu_pos_IsoPF04;
    Float_t b_recoMu_neg_IsoPF04;

    Float_t b_recoMu_sta_innerPosition_phi;
    Float_t b_recoMu_sta_innerPosition_eta;

    Float_t b_recoMu_sta_innerMomentum_phi;
    Float_t b_recoMu_sta_innerMomentum_pt;
    Float_t b_recoMu_sta_innerMomentum_eta;

    // positive GLB muons
    Bool_t  b_recoMu_pos_glb;
    Float_t b_recoMu_pos_glb_pt;
    Float_t b_recoMu_pos_glb_eta;
    Float_t b_recoMu_pos_glb_phi;
    Float_t b_recoMu_pos_glb_trk_pt;
    Float_t b_recoMu_pos_glb_trk_eta;
    Float_t b_recoMu_pos_glb_trk_phi;
    Bool_t  b_recoMu_pos_glb_pic;
    Float_t b_recoMu_pos_glb_pic_pt;
    Float_t b_recoMu_pos_glb_pic_eta;
    Float_t b_recoMu_pos_glb_pic_phi;

    // positive GEN muons matched to GLB muons
    Bool_t  b_recoMu_pos_glb_gen;
    Int_t   b_recoMu_pos_glb_gen_motherId;
    Float_t b_recoMu_pos_glb_gen_pt;
    Float_t b_recoMu_pos_glb_gen_eta;
    Float_t b_recoMu_pos_glb_gen_phi;

    // positive STA muons
    Bool_t  b_recoMu_pos_sta;
    Float_t b_recoMu_pos_sta_pt;
    Float_t b_recoMu_pos_sta_eta;
    Float_t b_recoMu_pos_sta_phi;

    // negative GLB muons
    Bool_t  b_recoMu_neg_glb;
    Float_t b_recoMu_neg_glb_pt;
    Float_t b_recoMu_neg_glb_eta;
    Float_t b_recoMu_neg_glb_phi;
    Float_t b_recoMu_neg_glb_trk_pt;
    Float_t b_recoMu_neg_glb_trk_eta;
    Float_t b_recoMu_neg_glb_trk_phi;
    Bool_t  b_recoMu_neg_glb_pic;
    Float_t b_recoMu_neg_glb_pic_pt;
    Float_t b_recoMu_neg_glb_pic_eta;
    Float_t b_recoMu_neg_glb_pic_phi;

    Bool_t  b_recoMu_neg_glb_gen;
    Int_t   b_recoMu_neg_glb_gen_motherId;
    Float_t b_recoMu_neg_glb_gen_pt;
    Float_t b_recoMu_neg_glb_gen_eta;
    Float_t b_recoMu_neg_glb_gen_phi;

    Bool_t  b_recoMu_neg_sta;
    Float_t b_recoMu_neg_sta_pt;
    Float_t b_recoMu_neg_sta_eta;
    Float_t b_recoMu_neg_sta_phi;

    Bool_t  b_recoMu_neg_tune;
    Float_t b_recoMu_neg_tune_pt;
    Float_t b_recoMu_neg_tune_eta;
    Float_t b_recoMu_neg_tune_phi;

    Bool_t  b_recoMu_pos_tune;
    Float_t b_recoMu_pos_tune_pt;
    Float_t b_recoMu_pos_tune_eta;
    Float_t b_recoMu_pos_tune_phi;

    // RECO dimuons
    TTree * m_tree_recoDimuons;
    Bool_t  b_recoDimu_glb;
    Float_t b_recoDimu_glb_pt;
    Float_t b_recoDimu_glb_eta;
    Float_t b_recoDimu_glb_phi;
    Float_t b_recoDimu_glb_m;
  

    Float_t b_recoDimu_glb_trk_pt;
    Float_t b_recoDimu_glb_trk_eta;
    Float_t b_recoDimu_glb_trk_phi;
    Float_t b_recoDimu_glb_trk_m;

    Bool_t  b_recoDimu_glb_pic;
    Float_t b_recoDimu_glb_pic_pt;
    Float_t b_recoDimu_glb_pic_eta;
    Float_t b_recoDimu_glb_pic_phi;
    Float_t b_recoDimu_glb_pic_m;

    Bool_t  b_recoDimu_glb_gen;
    Float_t b_recoDimu_glb_gen_pt;
    Float_t b_recoDimu_glb_gen_eta;
    Float_t b_recoDimu_glb_gen_phi;
    Float_t b_recoDimu_glb_gen_m;

    Bool_t  b_recoDimu_sta;
    Float_t b_recoDimu_sta_pt;
    Float_t b_recoDimu_sta_eta;
    Float_t b_recoDimu_sta_phi;
    Float_t b_recoDimu_sta_m;

    Bool_t  b_recoDimu_hyb;
    Float_t b_recoDimu_hyb_pt;
    Float_t b_recoDimu_hyb_eta;
    Float_t b_recoDimu_hyb_phi;
    Float_t b_recoDimu_hyb_sta_pt;
    Float_t b_recoDimu_hyb_sta_eta;
    Float_t b_recoDimu_hyb_sta_phi;

    Float_t b_recoDimu_hyb_glb_pt;
    Float_t b_recoDimu_hyb_glb_eta;
    Float_t b_recoDimu_hyb_glb_phi;


    Float_t b_recoDimu_hyb_m;
    Int_t b_recoDimu_hyb_sta_q;

    Bool_t  b_recoDimu_tune;
    Float_t b_recoDimu_tune_pt;
    Float_t b_recoDimu_tune_eta;
    Float_t b_recoDimu_tune_phi;
    Float_t b_recoDimu_tune_m;

    TRandom *random; 
    int randomInt;
};

MuAlAnalyzer::MuAlAnalyzer( const edm::ParameterSet& iConfig ) {

    random = new TRandom();
     

  m_debugLevel = iConfig.getParameter<int>("debugLevel");
  m_fillGenMuons = iConfig.getParameter<bool>("fillGenMuons");
  //primaryVerticesToken_ = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("primaryVertices"));
  if ( m_fillGenMuons ){
    m_genParticles = iConfig.getParameter<edm::InputTag>("genParticles");
    recoGenParticleToken_ = consumes<reco::GenParticleCollection,edm::InEvent>( m_genParticles );
  }

  m_fillRecoMuons = iConfig.getParameter<bool>("fillRecoMuons");
  if ( m_fillRecoMuons ) {
    m_recoMuons = iConfig.getParameter<edm::InputTag>("recoMuons");
    recoMuonCollectionToken_ = consumes<reco::MuonCollection,edm::InEvent>(m_recoMuons);
  }

  m_recoBeamSpot = iConfig.getParameter<edm::InputTag>("recoBeamSpot");
  recoBeamSpotToken_ = consumes<reco::BeamSpot,edm::InEvent>( m_recoBeamSpot );

  m_fillRecoDimuons = iConfig.getParameter<bool>("fillRecoDimuons");

  signalHltPaths_  = iConfig.getParameter<std::vector<std::string> >("signalHltPaths");
  m_trigRes         = consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("TriggerResults"));

  edm::Service<TFileService> fs;

  m_tree_info = fs->make<TTree>("Info", "Info");
  m_tree_info->Branch("fillGenMuons",&m_fillGenMuons,"fillGenMuons/O");
  m_tree_info->Branch("fillRecoMuons",&m_fillRecoMuons,"fillRecoMuons/O");
  m_tree_info->Branch("fillRecoDimuons",&m_fillRecoDimuons,"fillRecoDimuons/O");
  m_tree_info->Fill();

  m_tree_events = fs->make<TTree>("Events", "Events");
  if ( m_fillGenMuons    ) m_tree_events->Branch("n_genMuons",    &b_n_genMuons,   "n_genMuons/I");
  if ( m_fillRecoMuons   ) m_tree_events->Branch("n_recoMuons",   &b_n_recoMuons,  "n_recoMuons/I");
  if ( m_fillRecoDimuons ) m_tree_events->Branch("n_recoDimuons", &b_n_recoDimuons,"n_recoDimuons/I");

  if ( m_fillGenMuons ) {
    m_tree_genMuons = fs->make<TTree>("genMuons", "genMuons");
    m_tree_genMuons->Branch("q",&b_genMu_q,"q/I");
    m_tree_genMuons->Branch("motherId",&b_genMu_motherId,"motherId/I");
    m_tree_genMuons->Branch("pt",&b_genMu_pt,"pt/F");
    m_tree_genMuons->Branch("eta",&b_genMu_eta,"eta/F");
    m_tree_genMuons->Branch("phi",&b_genMu_phi,"phi/F");
  }

  if ( m_fillRecoMuons ) {
    m_tree_recoMuons = fs->make<TTree>("recoMuons", "recoMuons");

    m_tree_recoMuons->Branch("q",&b_recoMu_q,"q/I");
    m_tree_recoMuons->Branch("recoMu_IsoPF04",&b_recoMu_IsoPF04,"recoMu_IsoPF04/F");

    // GLB muons
    m_tree_recoMuons->Branch("glb",&b_recoMu_glb,"glb/O");
    m_tree_recoMuons->Branch("glb_pt",&b_recoMu_glb_pt,"glb_pt/F");
    m_tree_recoMuons->Branch("glb_eta",&b_recoMu_glb_eta,"glb_eta/F");
    m_tree_recoMuons->Branch("glb_phi",&b_recoMu_glb_phi,"glb_phi/F");
    m_tree_recoMuons->Branch("glb_phi_error",&b_recoMu_glb_phi_error,"glb_phi_error/F");
    m_tree_recoMuons->Branch("glb_nchi2",&b_recoMu_glb_nchi2,"glb_nchi2/F");
    m_tree_recoMuons->Branch("glb_chi2",&b_recoMu_glb_chi2,"glb_chi2/F");
    m_tree_recoMuons->Branch("glb_pt_error",&b_recoMu_glb_pterror,"glb_pt_error/F");
    m_tree_recoMuons->Branch("glb_qoverpterror",&b_recoMu_glb_qoverpterror,"glb_qoverpterror/F");
    m_tree_recoMuons->Branch("glb_nhits",&b_recoMu_glb_nhits,"glb_nhits/I");

    if ( m_fillGenMuons ) {
	// GEN muons matched to GLB muons
	m_tree_recoMuons->Branch("glb_gen",&b_recoMu_glb_gen,"glb_gen/O");
	m_tree_recoMuons->Branch("glb_gen_motherId",&b_recoMu_glb_gen_motherId,"glb_gen_motherId/I");
	m_tree_recoMuons->Branch("glb_gen_dR",&b_recoMu_glb_gen_dR,"glb_gen_dR/F");
	m_tree_recoMuons->Branch("glb_gen_pt",&b_recoMu_glb_gen_pt,"glb_gen_pt/F");
	m_tree_recoMuons->Branch("glb_gen_eta",&b_recoMu_glb_gen_eta,"glb_gen_eta/F");
	m_tree_recoMuons->Branch("glb_gen_phi",&b_recoMu_glb_gen_phi,"glb_gen_phi/F");
    }

    // inner tracks of the GLB muons
    m_tree_recoMuons->Branch("glb_trk_pt",&b_recoMu_glb_trk_pt,"glb_trk_pt/F");
    m_tree_recoMuons->Branch("glb_trk_eta",&b_recoMu_glb_trk_eta,"glb_trk_eta/F");
    m_tree_recoMuons->Branch("glb_trk_phi",&b_recoMu_glb_trk_phi,"glb_trk_phi/F");

    // "picky" tracks of the GLB muons
    m_tree_recoMuons->Branch("glb_pic",&b_recoMu_glb_pic,"glb_pic/O");
    m_tree_recoMuons->Branch("glb_pic_pt",&b_recoMu_glb_pic_pt,"glb_pic_pt/F");
    m_tree_recoMuons->Branch("glb_pic_eta",&b_recoMu_glb_pic_eta,"glb_pic_eta/F");
    m_tree_recoMuons->Branch("glb_pic_phi",&b_recoMu_glb_pic_phi,"glb_pic_phi/F");

    // STA muons
    m_tree_recoMuons->Branch("sta",&b_recoMu_sta,"sta/O");
    m_tree_recoMuons->Branch("sta_pt",&b_recoMu_sta_pt,"sta_pt/F");
    m_tree_recoMuons->Branch("sta_eta",&b_recoMu_sta_eta,"sta_eta/F");
    m_tree_recoMuons->Branch("sta_phi",&b_recoMu_sta_phi,"sta_phi/F");
    m_tree_recoMuons->Branch("sta_nchi2",&b_recoMu_sta_nchi2,"sta_nchi2/F");
    m_tree_recoMuons->Branch("sta_chi2",&b_recoMu_sta_chi2,"sta_chi2/F");

    m_tree_recoMuons->Branch("sta_innerPosition_phi",&b_recoMu_sta_innerPosition_phi,"sta_innerPosition_phi/F");
    m_tree_recoMuons->Branch("sta_innerPosition_eta",&b_recoMu_sta_innerPosition_eta,"sta_innerPosition_eta/F");
    m_tree_recoMuons->Branch("sta_innerMomentum_phi",&b_recoMu_sta_innerMomentum_phi,"sta_innerMomentum_phi/F");
    m_tree_recoMuons->Branch("sta_innerMomentum_pt",&b_recoMu_sta_innerMomentum_pt,"sta_innerMomentum_pt/F");
    m_tree_recoMuons->Branch("sta_innerMomentum_eta",&b_recoMu_sta_innerMomentum_eta,"sta_innerMomentum_eta/F");
  }

  if ( m_fillRecoDimuons ) {
    m_tree_recoDimuons = fs->make<TTree>("recoDimuons", "recoDimuons");
    m_tree_recoDimuons->Branch("recoMu_pos_IsoPF04",&b_recoMu_pos_IsoPF04,"recoMu_pos_IsoPF04/F");
    m_tree_recoDimuons->Branch("recoMu_neg_IsoPF04",&b_recoMu_neg_IsoPF04,"recoMu_neg_IsoPF04/F");
    m_tree_recoDimuons->Branch("recoMu_HLT_0", &b_HLT_0, "recoMu_HLT_0/O");
    m_tree_recoDimuons->Branch("recoMu_HLT_1", &b_HLT_1, "recoMu_HLT_1/O");
    m_tree_recoDimuons->Branch("recoMu_HLT_2", &b_HLT_2, "recoMu_HLT_2/O");

    // GLB muons: positive
    m_tree_recoDimuons->Branch("pos_glb",&b_recoMu_pos_glb,"pos_glb/O");
    m_tree_recoDimuons->Branch("pos_glb_pt",&b_recoMu_pos_glb_pt,"pos_glb_pt/F");
    m_tree_recoDimuons->Branch("pos_glb_eta",&b_recoMu_pos_glb_eta,"pos_glb_eta/F");
    m_tree_recoDimuons->Branch("pos_glb_phi",&b_recoMu_pos_glb_phi,"pos_glb_phi/F");
    if ( m_fillGenMuons ) {
	// GEN muons matched to GLB muons: positive
	m_tree_recoDimuons->Branch("pos_glb_gen",&b_recoMu_pos_glb_gen,"pos_glb_gen/O");
	m_tree_recoDimuons->Branch("pos_glb_gen_motherId",&b_recoMu_pos_glb_gen_motherId,"pos_glb_gen_motherId/I");
	m_tree_recoDimuons->Branch("pos_glb_gen_pt",&b_recoMu_pos_glb_gen_pt,"pos_glb_gen_pt/F");
	m_tree_recoDimuons->Branch("pos_glb_gen_eta",&b_recoMu_pos_glb_gen_eta,"pos_glb_gen_eta/F");
	m_tree_recoDimuons->Branch("pos_glb_gen_phi",&b_recoMu_pos_glb_gen_phi,"pos_glb_gen_phi/F");
    }
    // inner tracks of the GLB muons: positive
    m_tree_recoDimuons->Branch("pos_glb_trk_pt",&b_recoMu_pos_glb_trk_pt,"pos_glb_trk_pt/F");
    m_tree_recoDimuons->Branch("pos_glb_trk_eta",&b_recoMu_pos_glb_trk_eta,"pos_glb_trk_eta/F");
    m_tree_recoDimuons->Branch("pos_glb_trk_phi",&b_recoMu_pos_glb_trk_phi,"pos_glb_trk_phi/F");
    // "picky" tracks of the GLB muons: positive
    m_tree_recoDimuons->Branch("pos_glb_pic",&b_recoMu_pos_glb_pic,"pos_glb_pic/O");
    m_tree_recoDimuons->Branch("pos_glb_pic_pt",&b_recoMu_pos_glb_pic_pt,"pos_glb_pic_pt/F");
    m_tree_recoDimuons->Branch("pos_glb_pic_eta",&b_recoMu_pos_glb_pic_eta,"pos_glb_pic_eta/F");
    m_tree_recoDimuons->Branch("pos_glb_pic_phi",&b_recoMu_pos_glb_pic_phi,"pos_glb_pic_phi/F");
    // STA muons: positive
    m_tree_recoDimuons->Branch("pos_sta",&b_recoMu_pos_sta,"pos_sta/O");
    m_tree_recoDimuons->Branch("pos_sta_pt",&b_recoMu_pos_sta_pt,"pos_sta_pt/F");
    m_tree_recoDimuons->Branch("pos_sta_eta",&b_recoMu_pos_sta_eta,"pos_sta_eta/F");
    m_tree_recoDimuons->Branch("pos_sta_phi",&b_recoMu_pos_sta_phi,"pos_sta_phi/F");

    // GLB muons: negative
    m_tree_recoDimuons->Branch("neg_glb",&b_recoMu_neg_glb,"neg_glb/O");
    m_tree_recoDimuons->Branch("neg_glb_pt",&b_recoMu_neg_glb_pt,"neg_glb_pt/F");
    m_tree_recoDimuons->Branch("neg_glb_eta",&b_recoMu_neg_glb_eta,"neg_glb_eta/F");
    m_tree_recoDimuons->Branch("neg_glb_phi",&b_recoMu_neg_glb_phi,"neg_glb_phi/F");

    m_tree_recoDimuons->Branch("pos_tune",&b_recoMu_pos_tune,"pos_tune/O");
    m_tree_recoDimuons->Branch("pos_tune_pt",&b_recoMu_pos_tune_pt,"pos_tune_pt/F");
    m_tree_recoDimuons->Branch("pos_tune_eta",&b_recoMu_pos_tune_eta,"pos_tune_eta/F");
    m_tree_recoDimuons->Branch("pos_tune_phi",&b_recoMu_pos_tune_phi,"pos_tune_phi/F");

    m_tree_recoDimuons->Branch("neg_tune",&b_recoMu_neg_tune,"neg_tune/O");
    m_tree_recoDimuons->Branch("neg_tune_pt",&b_recoMu_neg_tune_pt,"neg_tune_pt/F");
    m_tree_recoDimuons->Branch("neg_tune_eta",&b_recoMu_neg_tune_eta,"neg_tune_eta/F");
    m_tree_recoDimuons->Branch("neg_tune_phi",&b_recoMu_neg_tune_phi,"neg_tune_phi/F");



    if ( m_fillGenMuons ) {
	// GEN muons matched to GLB muons: negative
	m_tree_recoDimuons->Branch("neg_glb_gen",&b_recoMu_neg_glb_gen,"neg_glb_gen/O");
	m_tree_recoDimuons->Branch("neg_glb_gen_motherId",&b_recoMu_neg_glb_gen_motherId,"neg_glb_gen_motherId/I");
	m_tree_recoDimuons->Branch("neg_glb_gen_pt",&b_recoMu_neg_glb_gen_pt,"neg_glb_gen_pt/F");
	m_tree_recoDimuons->Branch("neg_glb_gen_eta",&b_recoMu_neg_glb_gen_eta,"neg_glb_gen_eta/F");
	m_tree_recoDimuons->Branch("neg_glb_gen_phi",&b_recoMu_neg_glb_gen_phi,"neg_glb_gen_phi/F");
    }
    // inner tracks of the GLB muons: negative
    m_tree_recoDimuons->Branch("neg_glb_trk_pt",&b_recoMu_neg_glb_trk_pt,"neg_glb_trk_pt/F");
    m_tree_recoDimuons->Branch("neg_glb_trk_eta",&b_recoMu_neg_glb_trk_eta,"neg_glb_trk_eta/F");
    m_tree_recoDimuons->Branch("neg_glb_trk_phi",&b_recoMu_neg_glb_trk_phi,"neg_glb_trk_phi/F");
    // "picky" tracks of the GLB muons: negative
    m_tree_recoDimuons->Branch("neg_glb_pic",&b_recoMu_neg_glb_pic,"neg_glb_pic/O");
    m_tree_recoDimuons->Branch("neg_glb_pic_pt",&b_recoMu_neg_glb_pic_pt,"neg_glb_pic_pt/F");
    m_tree_recoDimuons->Branch("neg_glb_pic_eta",&b_recoMu_neg_glb_pic_eta,"neg_glb_pic_eta/F");
    m_tree_recoDimuons->Branch("neg_glb_pic_phi",&b_recoMu_neg_glb_pic_phi,"neg_glb_pic_phi/F");
    // STA muons: negative
    m_tree_recoDimuons->Branch("neg_sta",&b_recoMu_neg_sta,"neg_sta/O");
    m_tree_recoDimuons->Branch("neg_sta_pt",&b_recoMu_neg_sta_pt,"neg_sta_pt/F");
    m_tree_recoDimuons->Branch("neg_sta_eta",&b_recoMu_neg_sta_eta,"neg_sta_eta/F");
    m_tree_recoDimuons->Branch("neg_sta_phi",&b_recoMu_neg_sta_phi,"neg_sta_phi/F");

    // Dimuons constructed from two GLB muons
    m_tree_recoDimuons->Branch("glb",&b_recoDimu_glb,"glb/O");
    m_tree_recoDimuons->Branch("glb_pt",&b_recoDimu_glb_pt,"glb_pt/F");
    m_tree_recoDimuons->Branch("glb_eta",&b_recoDimu_glb_eta,"glb_eta/F");
    m_tree_recoDimuons->Branch("glb_phi",&b_recoDimu_glb_phi,"glb_phi/F");
    m_tree_recoDimuons->Branch("glb_m",&b_recoDimu_glb_m,"glb_m/F");
    
    if ( m_fillGenMuons ) {
	// Dimuons constructed from GEN muons matched to GLB muons
	m_tree_recoDimuons->Branch("glb_gen",&b_recoDimu_glb_gen,"glb_gen/O");
	m_tree_recoDimuons->Branch("glb_gen_pt",&b_recoDimu_glb_gen_pt,"glb_gen_pt/F");
	m_tree_recoDimuons->Branch("glb_gen_eta",&b_recoDimu_glb_gen_eta,"glb_gen_eta/F");
	m_tree_recoDimuons->Branch("glb_gen_phi",&b_recoDimu_glb_gen_phi,"glb_gen_phi/F");
	m_tree_recoDimuons->Branch("glb_gen_m",&b_recoDimu_glb_gen_m,"glb_gen_m/F");
    }
    // Dimuons constructed from inner tracks of the GLB muon
    m_tree_recoDimuons->Branch("glb_trk_pt",&b_recoDimu_glb_trk_pt,"glb_trk_pt/F");
    m_tree_recoDimuons->Branch("glb_trk_eta",&b_recoDimu_glb_trk_eta,"glb_trk_eta/F");
    m_tree_recoDimuons->Branch("glb_trk_phi",&b_recoDimu_glb_trk_phi,"glb_trk_phi/F");
    m_tree_recoDimuons->Branch("glb_trk_m",&b_recoDimu_glb_trk_m,"glb_trk_m/F");
    // Dimuons constructed from "picky" tracks of the GLB muons
    m_tree_recoDimuons->Branch("glb_pic",&b_recoDimu_glb_pic,"glb_pic/O");
    m_tree_recoDimuons->Branch("glb_pic_pt",&b_recoDimu_glb_pic_pt,"glb_pic_pt/F");
    m_tree_recoDimuons->Branch("glb_pic_eta",&b_recoDimu_glb_pic_eta,"glb_pic_eta/F");
    m_tree_recoDimuons->Branch("glb_pic_phi",&b_recoDimu_glb_pic_phi,"glb_pic_phi/F");
    m_tree_recoDimuons->Branch("glb_pic_m",&b_recoDimu_glb_pic_m,"glb_pic_m/F");
    // Dimuons constructed from two STA muons
    m_tree_recoDimuons->Branch("sta",&b_recoDimu_sta,"sta/O");
    m_tree_recoDimuons->Branch("sta_pt",&b_recoDimu_sta_pt,"sta_pt/F");
    m_tree_recoDimuons->Branch("sta_eta",&b_recoDimu_sta_eta,"sta_eta/F");
    m_tree_recoDimuons->Branch("sta_phi",&b_recoDimu_sta_phi,"sta_phi/F");
    m_tree_recoDimuons->Branch("sta_m",&b_recoDimu_sta_m,"sta_m/F");
    // Dimuons constructed from one STA and one GLB muons
    m_tree_recoDimuons->Branch("hyb",&b_recoDimu_hyb,"hyb/O");
    m_tree_recoDimuons->Branch("hyb_pt",&b_recoDimu_hyb_pt,"hyb_pt/F");
    m_tree_recoDimuons->Branch("hyb_eta",&b_recoDimu_hyb_eta,"hyb_eta/F");
    m_tree_recoDimuons->Branch("hyb_phi",&b_recoDimu_hyb_phi,"hyb_phi/F");
    m_tree_recoDimuons->Branch("hyb_sta_pt",&b_recoDimu_hyb_sta_pt,"hyb_sta_pt/F");
    m_tree_recoDimuons->Branch("hyb_sta_eta",&b_recoDimu_hyb_sta_eta,"hyb_sta_eta/F");
    m_tree_recoDimuons->Branch("hyb_sta_phi",&b_recoDimu_hyb_sta_phi,"hyb_sta_phi/F");

    m_tree_recoDimuons->Branch("hyb_glb_pt",&b_recoDimu_hyb_glb_pt,"hyb_glb_pt/F");
    m_tree_recoDimuons->Branch("hyb_glb_eta",&b_recoDimu_hyb_glb_eta,"hyb_glb_eta/F");
    m_tree_recoDimuons->Branch("hyb_glb_phi",&b_recoDimu_hyb_glb_phi,"hyb_glb_phi/F");

    m_tree_recoDimuons->Branch("hyb_m",&b_recoDimu_hyb_m,"hyb_m/F");
    m_tree_recoDimuons->Branch("hyb_q",&b_recoDimu_hyb_sta_q,"hyb_q/F");

    m_tree_recoDimuons->Branch("tune",&b_recoDimu_tune,"tune/O");
    m_tree_recoDimuons->Branch("tune_pt",&b_recoDimu_tune_pt,"tune_pt/F");
    m_tree_recoDimuons->Branch("tune_eta",&b_recoDimu_tune_eta,"tune_eta/F");
    m_tree_recoDimuons->Branch("tune_phi",&b_recoDimu_tune_phi,"tune_phi/F");
    m_tree_recoDimuons->Branch("tune_m",&b_recoDimu_tune_m,"tune_m/F");


  }
}

MuAlAnalyzer::~MuAlAnalyzer() {

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

bool RecoPtSort(const reco::Muon *mu1, const reco::Muon *mu2){ 
  if (mu1->pt() > mu2->pt()) return true;
  else return false;
}

bool GenPtSort(const reco::GenParticle *p1, const reco::GenParticle *p2){ 
  if (p1->pt() > p2->pt()) return true;
  else return false;
}

//******************************************************************************
// Auxiliary function: Calculate difference between two angles: -PI < phi < PI  
//******************************************************************************
double My_dPhi (double phi1, double phi2) {
  double dPhi = phi1 - phi2;
  if (dPhi >  M_PI) dPhi -= 2.*M_PI;
  if (dPhi < -M_PI) dPhi += 2.*M_PI;
  return dPhi;
}

// ------------ method called for each event  ------------
void MuAlAnalyzer::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup ) {


  edm::Handle<edm::TriggerResults> TrResults;
  iEvent.getByToken( m_trigRes, TrResults);
  const edm::TriggerNames& trigNameStr = iEvent.triggerNames(*TrResults);
  unsigned int trgSize = trigNameStr.size();
  /*for (unsigned int itrig = 0; itrig != trgSize; ++itrig){
    TString trigName = trigNameStr.triggerName(itrig);
    std::cout << trigName << std::endl;}*/
  b_HLT_0 = false; b_HLT_1 = false; b_HLT_2 = false;
  if ( signalHltPaths_.size() > 0){
    const std::string& s0 = signalHltPaths_[0];
    if (trigNameStr.triggerIndex(s0) != trgSize){ b_HLT_0 = true; std::cout << "HLT 1 fired" << std::endl;}
  }
  if ( signalHltPaths_.size() > 1){
    const std::string& s1 = signalHltPaths_[1];
    if (trigNameStr.triggerIndex(s1) != trgSize) b_HLT_1 = true;
  }
  if ( signalHltPaths_.size() > 2){
    const std::string& s2 = signalHltPaths_[2];
    if (trigNameStr.triggerIndex(s2) != trgSize) b_HLT_2 = true;
  }

  //****************************************************************************
  //                              GEN Muons                                     
  //****************************************************************************

  std::vector<const reco::GenParticle*> genMuons;
  std::vector<int>  genMuonsMotherId;
  std::vector<int>  genMuonsMatchToGlb;

  if ( m_fillGenMuons ) {
    edm::Handle<reco::GenParticleCollection> genParticles;
    iEvent.getByToken(recoGenParticleToken_, genParticles);

    // Loop over all gen particles
    int counterGenParticle = 0;
    for(reco::GenParticleCollection::const_iterator iGenParticle = genParticles->begin();  iGenParticle != genParticles->end();  ++iGenParticle) {
	counterGenParticle++;
	//    std::cout << counterGenParticle << " " << iGenParticle->status() << " " << iGenParticle->pdgId() << " " << iGenParticle->vx() << " " << iGenParticle->vy() << " " << iGenParticle->vz() << std::endl;
	// Check if gen particle is muon (pdgId = +/-13) and stable (status = 1)
	if ( fabs( iGenParticle->pdgId() ) == 13 && iGenParticle->status() == 1 ) {
	  // Store the muon (stable, first in chain) into vector
	  genMuons.push_back(&(*iGenParticle));

	  // Find mother of the muon
	  // Mother of the muon can be muon. Find the last muon in this chain: genMuonCand
	  // Example: a1 -> mu+ (status = 3) mu- (status = 3)
	  //          mu- (status = 3) -> mu- (status = 2) -> mu- (status = 1)
	  const reco::Candidate *genMuonCand = &(*iGenParticle);
	  bool isMuonMother = true;
	  while(isMuonMother) {
	    isMuonMother = false;
	    for ( size_t iMother = 0; iMother < genMuonCand->numberOfMothers(); iMother++ ) {
		if ( fabs( genMuonCand->mother(iMother)->pdgId() ) == 13 ) {
		  isMuonMother = true;
		  genMuonCand = genMuonCand->mother(iMother);
		}
	    }
	  }

	  // Access real (non-muon) mothers of the muon (here we use genMuonCand)
	  Int_t genMuonsNMothers = genMuonCand->numberOfMothers();
	  if ( genMuonsNMothers >= 1 ) {
	    genMuonsMotherId.push_back( genMuonCand->mother(0)->pdgId() );
	    if ( genMuonsNMothers > 1 ) {
		std::cerr << "WARNING! GEN muon got more than 1 mothers" << std::endl;
	    }
	  } else {
	    genMuonsMotherId.push_back( 0 );
	    std::cerr << "WARNING! GEN muon got NO mothers" << std::endl;
	  }
	}
    }

    b_n_genMuons  = genMuons.size();
    if ( m_debugLevel > 10 ) std::cout << "GEN muons: " << b_n_genMuons << std::endl;
    // Set GEN muons to branches, fill tree and print stored information
    for ( unsigned j = 0; j < genMuons.size(); ++j ) {
	b_genMu_q        = genMuons[j]->charge();
	b_genMu_motherId = genMuonsMotherId[j];
	b_genMu_pt       = genMuons[j]->pt();
	b_genMu_eta      = genMuons[j]->eta();
	b_genMu_phi      = genMuons[j]->phi();

	m_tree_genMuons->Fill();

	if ( m_debugLevel > 10 ) std::cout << " " << j << ":"
	  << " q "        << b_genMu_q
	    << " motherId " << b_genMu_motherId
	    << " pt "       << b_genMu_pt
	    << " eta "      << b_genMu_eta
	    << " phi "      << b_genMu_phi
	    << std::endl;
    }

    // vector GEN muons matched to GLB muons: preset to default "-1"
    for ( unsigned j = 0; j < genMuons.size(); ++j ) genMuonsMatchToGlb.push_back(-1);
  }

  //****************************************************************************
  //                              RECO Muons                                    
  //****************************************************************************

  // Vertex
  //edm::Handle<reco::VertexCollection> primaryVertices;
  //iEvent.getByToken(primaryVerticesToken_, primaryVertices);
  //if (primaryVertices->empty()) return; // skip the event if no PV found
  //const reco::Vertex &PV = primaryVertices->front();
  // Muons
  std::vector<const reco::Muon*> recoMuonsSelected;
  std::vector<int> recoMuonsGlbMatchToGen;
  bool ZtightSele = true;
  bool ZtightSele_pass = false;

  if ( m_fillRecoMuons ) {

    edm::Handle<reco::MuonCollection> recoMuonCollection;
    iEvent.getByToken(recoMuonCollectionToken_, recoMuonCollection);

    edm::Handle<reco::BeamSpot> beamspot;
    iEvent.getByToken(recoBeamSpotToken_, beamspot);
    if ( recoMuonCollection.isValid() ) {
	for (reco::MuonCollection::const_iterator Mymuon = recoMuonCollection->begin();  Mymuon != recoMuonCollection->end();  ++Mymuon) {

	  if ( Mymuon->isGlobalMuon() && Mymuon->isStandAloneMuon() ) {
	    if ( Mymuon->globalTrack()->normalizedChi2()   < 10
		  && Mymuon->innerTrack()->numberOfValidHits() > 10
		  && Mymuon->numberOfMatchedStations() > 1
		  && fabs( Mymuon->innerTrack()->dxy( beamspot->position() ) ) < 0.2 && Mymuon->innerTrack()->pt() > 30.0 && TMath::Abs(Mymuon->innerTrack()->eta()) < 2.4) {
		recoMuonsSelected.push_back(&*Mymuon);
	    }
	  }
	}
    }

    if( ZtightSele ){
	if( recoMuonsSelected.size()==2 ){
	  TLorentzVector mu1, mu2;
	  mu1.SetPtEtaPhiM( recoMuonsSelected[0]->innerTrack()->pt(), recoMuonsSelected[0]->innerTrack()->eta(), recoMuonsSelected[0]->innerTrack()->phi(), 0.105658);
	  mu2.SetPtEtaPhiM( recoMuonsSelected[1]->innerTrack()->pt(), recoMuonsSelected[1]->innerTrack()->eta(), recoMuonsSelected[1]->innerTrack()->phi(), 0.105658);
	  if(recoMuonsSelected[0]->charge()*recoMuonsSelected[1]->charge()==-1 and fabs((mu1+mu2).M()-91)<30 ){
	    ZtightSele_pass = true;
	  }
	}
    }
    if ((ZtightSele and ZtightSele_pass) or !ZtightSele){

	b_n_recoMuons = recoMuonsSelected.size();
	// vector GEN muons matched to GLB muons: preset to default "-1"
	for ( unsigned i = 0; i < recoMuonsSelected.size(); ++i ) recoMuonsGlbMatchToGen.push_back(-1);

	if ( m_debugLevel > 10 ) std::cout << "RECO muons selected: " << b_n_recoMuons << std::endl;

	// Loop over selected RECO muons
	// Set branches, fill tree and print stored information
	for ( unsigned i = 0; i < recoMuonsSelected.size(); ++i ) {

	  b_recoMu_q = recoMuonsSelected[i]->charge();
	  //https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Tight_Muon
	  //https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Muon_Isolation
	  //bool isTight = muon::isTightMuon(PV,recoMuonsSelected[i]);
	  //std::cout<<"b_recoMu_IsoPF04 "<<recoMuonsSelected[i]->pfIsolationR04().sumChargedHadronPt<<" + "<<std::max(0., recoMuonsSelected[i]->pfIsolationR04().sumNeutralHadronEt + recoMuonsSelected[i]->pfIsolationR04().sumPhotonEt - 0.5*recoMuonsSelected[i]->pfIsolationR04().sumPUPt)<<" / "<<recoMuonsSelected[i]->pt()<<std::endl;
	  b_recoMu_IsoPF04 = (recoMuonsSelected[i]->pfIsolationR04().sumChargedHadronPt + std::max(0., recoMuonsSelected[i]->pfIsolationR04().sumNeutralHadronEt + recoMuonsSelected[i]->pfIsolationR04().sumPhotonEt - 0.5*recoMuonsSelected[i]->pfIsolationR04().sumPUPt))/recoMuonsSelected[i]->pt();

	  if ( recoMuonsSelected[i]->isGlobalMuon() ) {
	    b_recoMu_glb       = true;

	    b_recoMu_glb_pt    = recoMuonsSelected[i]->globalTrack()->pt();
	    b_recoMu_glb_eta   = recoMuonsSelected[i]->globalTrack()->eta();
	    b_recoMu_glb_phi   = recoMuonsSelected[i]->globalTrack()->phi();
	    b_recoMu_glb_nchi2 = recoMuonsSelected[i]->globalTrack()->normalizedChi2();
	    b_recoMu_glb_phi_error  = recoMuonsSelected[i]->globalTrack()->phiError();
	    b_recoMu_glb_chi2  = recoMuonsSelected[i]->globalTrack()->chi2();
	    b_recoMu_glb_pterror  = recoMuonsSelected[i]->globalTrack()->ptError();
	    b_recoMu_glb_qoverpterror  = recoMuonsSelected[i]->globalTrack()->qoverpError();
	    b_recoMu_glb_nhits  = recoMuonsSelected[i]->globalTrack()->numberOfValidHits();

	    b_recoMu_glb_trk_pt  = recoMuonsSelected[i]->innerTrack()->pt();
	    b_recoMu_glb_trk_eta = recoMuonsSelected[i]->innerTrack()->eta();
	    b_recoMu_glb_trk_phi = recoMuonsSelected[i]->innerTrack()->phi();

	    if( recoMuonsSelected[i]->pickyTrack().isNonnull() ) {
		b_recoMu_glb_pic     = true;
		b_recoMu_glb_pic_pt  = recoMuonsSelected[i]->pickyTrack()->pt();
		b_recoMu_glb_pic_eta = recoMuonsSelected[i]->pickyTrack()->eta();
		b_recoMu_glb_pic_phi = recoMuonsSelected[i]->pickyTrack()->phi();
	    } else {
		b_recoMu_glb_pic     = false;
		b_recoMu_glb_pic_pt  = -1.0;
		b_recoMu_glb_pic_eta = 10.0;
		b_recoMu_glb_pic_phi =  5.0;
	    }

	    // Match GEN to GLB muons
	    if ( m_fillGenMuons ) {     
		int     j_min       =   -1; // index of genMuons[j_min] with smallest dR
		Float_t dR_min      = 10.0; // large start value for smallest dR
		Float_t dR_limit    =  0.1;
		b_recoMu_glb_gen_dR = -1.0;

		// loop over GEN muons and find a GEN muon with smallest dR w.r.t. the GLB muon [i]
		for ( unsigned j = 0; j < genMuons.size(); ++j ) {
		  // Use only GEN muons that are NOT already matched to GLB muons
		  if ( genMuonsMatchToGlb[j] == -1 ) {
		    Float_t dEta = recoMuonsSelected[i]->globalTrack()->eta() - genMuons[j]->eta();
		    Float_t dPhi = My_dPhi( recoMuonsSelected[i]->globalTrack()->phi(), genMuons[j]->phi() );
		    Float_t dR = sqrt( dEta*dEta + dPhi*dPhi );
		    if ( dR < dR_min ) {
			dR_min = dR;
			j_min  = j;
		    }
		  }
		}

		// store the smallest dR for possible future analysis
		if ( j_min != -1 ) b_recoMu_glb_gen_dR = dR_min;

		// check if GEN muon with smalles dR is matched to the GLB muon [i]
		if ( j_min != -1 && dR_min < dR_limit && recoMuonsSelected[i]->charge() == genMuons[j_min]->charge() ) {
		  genMuonsMatchToGlb[j_min] = i;
		  recoMuonsGlbMatchToGen[i] = j_min;
		  b_recoMu_glb_gen          = true;
		  b_recoMu_glb_gen_motherId = genMuonsMotherId[j_min];
		  b_recoMu_glb_gen_pt       = genMuons[j_min]->pt();
		  b_recoMu_glb_gen_eta      = genMuons[j_min]->eta();
		  b_recoMu_glb_gen_phi      = genMuons[j_min]->phi();
		} else {
		  b_recoMu_glb_gen          = false;
		  b_recoMu_glb_gen_motherId =    0;
		  b_recoMu_glb_gen_pt       = -1.0;
		  b_recoMu_glb_gen_eta      = 10.0;
		  b_recoMu_glb_gen_phi      =  5.0;
		}
	    }
	  } else {
	    b_recoMu_glb       = false;
	    b_recoMu_glb_pt    = -1.0;
	    b_recoMu_glb_eta   = 10.0;
	    b_recoMu_glb_phi   =  5.0;
	    b_recoMu_glb_phi_error = -1.0;
	    b_recoMu_glb_nchi2 = -1.0;
	    b_recoMu_glb_chi2  = -1.0;
	    b_recoMu_glb_pterror  = -1.0;
	    b_recoMu_glb_qoverpterror = -1.0;
	    b_recoMu_glb_nhits  = -1.0;

	    b_recoMu_glb_trk_pt    = -1.0;
	    b_recoMu_glb_trk_eta   = 10.0;
	    b_recoMu_glb_trk_phi   =  5.0;

	    b_recoMu_glb_pic_pt    = -1.0;
	    b_recoMu_glb_pic_eta   = 10.0;
	    b_recoMu_glb_pic_phi   =  5.0;
	  }

	  if (recoMuonsSelected[i]->isStandAloneMuon()) {
	    b_recoMu_sta       = true;
	    b_recoMu_sta_pt    = recoMuonsSelected[i]->standAloneMuon()->pt();
	    b_recoMu_sta_eta   = recoMuonsSelected[i]->standAloneMuon()->eta();
	    b_recoMu_sta_phi   = recoMuonsSelected[i]->standAloneMuon()->phi();
	    b_recoMu_sta_nchi2 = recoMuonsSelected[i]->standAloneMuon()->normalizedChi2();
	    b_recoMu_sta_chi2  = recoMuonsSelected[i]->standAloneMuon()->chi2();

	    b_recoMu_sta_innerPosition_phi = recoMuonsSelected[i]->outerTrack()->innerPosition().phi();
	    b_recoMu_sta_innerPosition_eta = recoMuonsSelected[i]->outerTrack()->innerPosition().eta();
	    b_recoMu_sta_innerMomentum_phi = recoMuonsSelected[i]->outerTrack()->innerMomentum().phi();
	    b_recoMu_sta_innerMomentum_pt = recoMuonsSelected[i]->outerTrack()->innerMomentum().Rho();
	    b_recoMu_sta_innerMomentum_eta = recoMuonsSelected[i]->outerTrack()->innerMomentum().eta();

	  } else {
	    b_recoMu_sta       = false;
	    b_recoMu_sta_pt    = -1.0;
	    b_recoMu_sta_eta   = 10.0;
	    b_recoMu_sta_phi   =  5.0;
	    b_recoMu_sta_nchi2 = -1.0;
	    b_recoMu_sta_chi2  = -1.0;

	    b_recoMu_sta_innerPosition_phi = -100.0 ;
	    b_recoMu_sta_innerPosition_eta = -100.0 ;
	    b_recoMu_sta_innerMomentum_phi = -100.0 ;
	    b_recoMu_sta_innerMomentum_pt = -100.0 ;
	    b_recoMu_sta_innerMomentum_eta = -100.0 ;
	  }

	  m_tree_recoMuons->Fill();

	  if ( m_debugLevel > 10 ) std::cout << " " << i << ":"
	    << " q "        << b_recoMu_q << "\n"
		<< "     IsoPF04 " << b_recoMu_IsoPF04
		<< "     glb " << b_recoMu_glb
		<< " pt " << b_recoMu_glb_pt
		<< " eta " << b_recoMu_glb_eta
		<< " phi " << b_recoMu_glb_phi
		<< " phi error " << b_recoMu_glb_phi_error << "\n"
		<< " nchi2 " << b_recoMu_glb_nchi2
		<< " chi2 " << b_recoMu_glb_chi2 << "\n"
		<< " pT error " << b_recoMu_glb_pterror << "\n"
		<< " q over pt error " << b_recoMu_glb_qoverpterror << "\n"
		<< " nhits " << b_recoMu_glb_nhits << "\n"
		<< "       trk pt " <<  b_recoMu_glb_trk_pt
		<< " eta " << b_recoMu_glb_trk_eta
		<< " phi " << b_recoMu_glb_trk_phi << "\n"
		<< "       pic pt " << b_recoMu_glb_pic_pt
		<< " eta " << b_recoMu_glb_pic_eta
		<< " phi " << b_recoMu_glb_pic_phi << "\n"
		<< "       glb_gen " << b_recoMu_glb_gen
		<< " motherId " << b_recoMu_glb_gen_motherId
		<< " dR " << b_recoMu_glb_gen_dR
		<< " pt "       << b_recoMu_glb_gen_pt
		<< " eta "      << b_recoMu_glb_gen_eta
		<< " phi "      << b_recoMu_glb_gen_phi << "\n"
		<< "     sta " <<  b_recoMu_sta
		<< " pt " << b_recoMu_sta_pt
		<< " eta " << b_recoMu_sta_eta
		<< " phi " << b_recoMu_sta_phi
		<< " nchi2 " << b_recoMu_sta_nchi2
		<< " chi2 " << b_recoMu_sta_chi2
		<< " innerPosition phi " << b_recoMu_sta_innerPosition_phi
		<< " innerPosition eta " << b_recoMu_sta_innerPosition_eta
		<< " innerMomentum phi " << b_recoMu_sta_innerMomentum_phi
		<< " innerMomentum pt  " << b_recoMu_sta_innerMomentum_pt 
		<< " innerMomentum eta " << b_recoMu_sta_innerMomentum_eta
		<< std::endl;
	}
    }
  }

  if (m_fillRecoMuons && m_fillRecoDimuons && (((ZtightSele and ZtightSele_pass) or !ZtightSele))) {

    std::vector<int> iPos;
    std::vector<int> iNeg;

    // Loop over all pairs of selected RECO muons
    for ( unsigned i = 0; i < recoMuonsSelected.size()-1; ++i ) {
	for ( unsigned j = i+1; j < recoMuonsSelected.size(); ++j ) {
	  // Select only pairs with opposite charge
	  if ( recoMuonsSelected[i]->charge()*recoMuonsSelected[j]->charge() == -1 ) {

	    b_n_recoDimuons = b_n_recoDimuons + 1;

	    if ( recoMuonsSelected[i]->charge() > 0 ) {
		iPos.push_back(i);
		iNeg.push_back(j);
	    } else {
		iNeg.push_back(i);
		iPos.push_back(j);
	    }
	  }
	}
    }

    b_n_recoDimuons = iPos.size();
    if ( m_debugLevel > 10 ) std::cout << "RECO dimuons: " << b_n_recoDimuons << std::endl;

    const reco::Muon* recoMuonPos;
    const reco::Muon* recoMuonNeg;

    // Loop over RECO dimuons
    for ( unsigned i = 0; i < iPos.size(); ++i ) {

	recoMuonPos = recoMuonsSelected[ iPos[i] ];
	recoMuonNeg = recoMuonsSelected[ iNeg[i] ];


	//https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Tight_Muon
	//https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Muon_Isolation
	//bool isTight = muon::isTightMuon(PV,recoMuonsSelected[i]);
	b_recoMu_pos_IsoPF04 = (recoMuonPos->pfIsolationR04().sumChargedHadronPt + std::max(0., recoMuonPos->pfIsolationR04().sumNeutralHadronEt + recoMuonPos->pfIsolationR04().sumPhotonEt - 0.5*recoMuonPos->pfIsolationR04().sumPUPt))/recoMuonPos->pt();
	b_recoMu_neg_IsoPF04 = (recoMuonNeg->pfIsolationR04().sumChargedHadronPt + std::max(0., recoMuonNeg->pfIsolationR04().sumNeutralHadronEt + recoMuonNeg->pfIsolationR04().sumPhotonEt - 0.5*recoMuonNeg->pfIsolationR04().sumPUPt))/recoMuonNeg->pt();

	// Set branches for positive GLB muon
	if ( recoMuonPos->isGlobalMuon() ) {
	  b_recoMu_pos_glb     = true;

	  b_recoMu_pos_glb_pt  = recoMuonPos->globalTrack()->pt();
	  b_recoMu_pos_glb_eta = recoMuonPos->globalTrack()->eta();
	  b_recoMu_pos_glb_phi = recoMuonPos->globalTrack()->phi();

	  b_recoMu_pos_glb_trk_pt  = recoMuonPos->innerTrack()->pt();
	  b_recoMu_pos_glb_trk_eta = recoMuonPos->innerTrack()->eta();
	  b_recoMu_pos_glb_trk_phi = recoMuonPos->innerTrack()->phi();


          if ( recoMuonPos->tunePMuonBestTrack().isNonnull() ) {
	    b_recoMu_pos_tune = true;
	    b_recoMu_pos_tune_pt = recoMuonPos->tunePMuonBestTrack()->pt();
	    b_recoMu_pos_tune_eta = recoMuonPos->tunePMuonBestTrack()->eta();
	    b_recoMu_pos_tune_phi = recoMuonPos->tunePMuonBestTrack()->phi();
	  } else {
             b_recoMu_pos_tune = false;
	     b_recoMu_pos_tune_pt = -1.0;
	     b_recoMu_pos_tune_eta = 10.0;
	     b_recoMu_pos_tune_phi = 5.0;
          }




	  if ( recoMuonPos->pickyTrack().isNonnull() ) {
	    b_recoMu_pos_glb_pic     = true;
	    b_recoMu_pos_glb_pic_pt  = recoMuonPos->pickyTrack()->pt();
	    b_recoMu_pos_glb_pic_eta = recoMuonPos->pickyTrack()->eta();
	    b_recoMu_pos_glb_pic_phi = recoMuonPos->pickyTrack()->phi();
	  } else {
	    b_recoMu_pos_glb_pic     = false;
	    b_recoMu_pos_glb_pic_pt  = -1.0;
	    b_recoMu_pos_glb_pic_eta = 10.0;
	    b_recoMu_pos_glb_pic_phi =  5.0;
	  }

	  if ( m_fillGenMuons ) {
	    int iPosGen = recoMuonsGlbMatchToGen[ iPos[i] ];
	    if ( iPosGen != -1 ) {
		b_recoMu_pos_glb_gen = true;
		b_recoMu_pos_glb_gen_motherId  = genMuonsMotherId[ iPosGen ];
		b_recoMu_pos_glb_gen_pt        = genMuons[ iPosGen ]->pt();
		b_recoMu_pos_glb_gen_eta       = genMuons[ iPosGen ]->eta();
		b_recoMu_pos_glb_gen_phi       = genMuons[ iPosGen ]->phi();
	    } else {
		b_recoMu_pos_glb_gen = false;
		b_recoMu_pos_glb_gen_motherId  =    0;
		b_recoMu_pos_glb_gen_pt        = -1.0;
		b_recoMu_pos_glb_gen_eta       = 10.0;
		b_recoMu_pos_glb_gen_phi       =  5.0;
	    }
	  }
	} else {
	  b_recoMu_pos_glb     = false;

	  b_recoMu_pos_glb_pt  = -1.0;
	  b_recoMu_pos_glb_eta = 10.0;
	  b_recoMu_pos_glb_phi =  5.0;

	  b_recoMu_pos_glb_trk_pt  = -1.0;
	  b_recoMu_pos_glb_trk_eta = 10.0;
	  b_recoMu_pos_glb_trk_phi =  5.0;

	  b_recoMu_pos_glb_pic     = false;
	  b_recoMu_pos_glb_pic_pt  = -1.0;
	  b_recoMu_pos_glb_pic_eta = 10.0;
	  b_recoMu_pos_glb_pic_phi =  5.0;

	  if ( m_fillGenMuons ) {
	    b_recoMu_pos_glb_gen = false;
	    b_recoMu_pos_glb_gen_motherId  =    0;
	    b_recoMu_pos_glb_gen_pt        = -1.0;
	    b_recoMu_pos_glb_gen_eta       = 10.0;
	    b_recoMu_pos_glb_gen_phi       =  5.0;
	  }
	}

	// Set branches for negative GLB muon
	if ( recoMuonNeg->isGlobalMuon() ) {
	  b_recoMu_neg_glb     = true;

	  b_recoMu_neg_glb_pt  = recoMuonNeg->globalTrack()->pt();
	  b_recoMu_neg_glb_eta = recoMuonNeg->globalTrack()->eta();
	  b_recoMu_neg_glb_phi = recoMuonNeg->globalTrack()->phi();

	  b_recoMu_neg_glb_trk_pt  = recoMuonNeg->innerTrack()->pt();
	  b_recoMu_neg_glb_trk_eta = recoMuonNeg->innerTrack()->eta();
	  b_recoMu_neg_glb_trk_phi = recoMuonNeg->innerTrack()->phi();


          if ( recoMuonNeg->tunePMuonBestTrack().isNonnull() ) {
	    b_recoMu_neg_tune = true;
	    b_recoMu_neg_tune_pt = recoMuonNeg->tunePMuonBestTrack()->pt();
	    b_recoMu_neg_tune_eta = recoMuonNeg->tunePMuonBestTrack()->eta();
	    b_recoMu_neg_tune_phi = recoMuonNeg->tunePMuonBestTrack()->phi();
	  } else {
             b_recoMu_neg_tune = false;
	     b_recoMu_neg_tune_pt = -1.0;
	     b_recoMu_neg_tune_eta = 10.0;
	     b_recoMu_neg_tune_phi = 5.0;
          }

	  if ( recoMuonNeg->pickyTrack().isNonnull() ) {
	    b_recoMu_neg_glb_pic     = true;
	    b_recoMu_neg_glb_pic_pt  = recoMuonNeg->pickyTrack()->pt();
	    b_recoMu_neg_glb_pic_eta = recoMuonNeg->pickyTrack()->eta();
	    b_recoMu_neg_glb_pic_phi = recoMuonNeg->pickyTrack()->phi();
	  } else {
	    b_recoMu_neg_glb_pic     = false;
	    b_recoMu_neg_glb_pic_pt  = -1.0;
	    b_recoMu_neg_glb_pic_eta = 10.0;
	    b_recoMu_neg_glb_pic_phi =  5.0;
	  }

	  if ( m_fillGenMuons ) {
	    int iNegGen = recoMuonsGlbMatchToGen[ iNeg[i] ];
	    if ( iNegGen != -1 ) {
		b_recoMu_neg_glb_gen = true;
		b_recoMu_neg_glb_gen_motherId  = genMuonsMotherId[ iNegGen ];
		b_recoMu_neg_glb_gen_pt        = genMuons[ iNegGen ]->pt();
		b_recoMu_neg_glb_gen_eta       = genMuons[ iNegGen ]->eta();
		b_recoMu_neg_glb_gen_phi       = genMuons[ iNegGen ]->phi();
	    } else {
		b_recoMu_neg_glb_gen = false;
		b_recoMu_neg_glb_gen_motherId  =    0;
		b_recoMu_neg_glb_gen_pt        = -1.0;
		b_recoMu_neg_glb_gen_eta       = 10.0;
		b_recoMu_neg_glb_gen_phi       =  5.0;
	    }
	  }
	} else {
	  b_recoMu_neg_glb     = false;

	  b_recoMu_neg_glb_pt  = -1.0;
	  b_recoMu_neg_glb_eta = 10.0;
	  b_recoMu_neg_glb_phi =  5.0;

	  b_recoMu_neg_glb_trk_pt  = -1.0;
	  b_recoMu_neg_glb_trk_eta = 10.0;
	  b_recoMu_neg_glb_trk_phi =  5.0;

	  b_recoMu_neg_glb_pic     = false;
	  b_recoMu_neg_glb_pic_pt  = -1.0;
	  b_recoMu_neg_glb_pic_eta = 10.0;
	  b_recoMu_neg_glb_pic_phi =  5.0;

	  if ( m_fillGenMuons ) {
	    b_recoMu_neg_glb_gen = false;
	    b_recoMu_neg_glb_gen_motherId  =    0;
	    b_recoMu_neg_glb_gen_pt        = -1.0;
	    b_recoMu_neg_glb_gen_eta       = 10.0;
	    b_recoMu_neg_glb_gen_phi       =  5.0;
	  }
	}

	// Calculate dimuon branches
	if ( b_recoMu_pos_glb == true && b_recoMu_neg_glb == true ) {
	  b_recoDimu_glb     = true;

	  TLorentzVector tLV_recoMuonPos_glb, tLV_recoMuonNeg_glb, tLV_dimu_glb;
	  tLV_recoMuonPos_glb.SetPtEtaPhiM(b_recoMu_pos_glb_pt, b_recoMu_pos_glb_eta, b_recoMu_pos_glb_phi, 0.105658);
	  tLV_recoMuonNeg_glb.SetPtEtaPhiM(b_recoMu_neg_glb_pt, b_recoMu_neg_glb_eta, b_recoMu_neg_glb_phi, 0.105658);
	  tLV_dimu_glb = tLV_recoMuonPos_glb + tLV_recoMuonNeg_glb;

	  b_recoDimu_glb_pt  = tLV_dimu_glb.Pt();
	  b_recoDimu_glb_eta = tLV_dimu_glb.Eta();
	  b_recoDimu_glb_phi = tLV_dimu_glb.Phi();
	  b_recoDimu_glb_m   = tLV_dimu_glb.M();

	  TLorentzVector tLV_recoMuonPos_trk, tLV_recoMuonNeg_trk, tLV_dimu_trk;
	  tLV_recoMuonPos_trk.SetPtEtaPhiM(b_recoMu_pos_glb_trk_pt, b_recoMu_pos_glb_trk_eta, b_recoMu_pos_glb_trk_phi, 0.105658);
	  tLV_recoMuonNeg_trk.SetPtEtaPhiM(b_recoMu_neg_glb_trk_pt, b_recoMu_neg_glb_trk_eta, b_recoMu_neg_glb_trk_phi, 0.105658);
	  tLV_dimu_trk = tLV_recoMuonPos_trk + tLV_recoMuonNeg_trk;

	  b_recoDimu_glb_trk_pt  = tLV_dimu_trk.Pt();
	  b_recoDimu_glb_trk_eta = tLV_dimu_trk.Eta();
	  b_recoDimu_glb_trk_phi = tLV_dimu_trk.Phi();
	  b_recoDimu_glb_trk_m   = tLV_dimu_trk.M();

	  if ( b_recoMu_pos_tune == true && b_recoMu_neg_tune == true ) {
	    TLorentzVector tLV_recoMuonPos_tune, tLV_recoMuonNeg_tune, tLV_dimu_tune;
	    tLV_recoMuonPos_tune.SetPtEtaPhiM(b_recoMu_pos_tune_pt, b_recoMu_pos_tune_eta, b_recoMu_pos_tune_phi, 0.105658);
	    tLV_recoMuonNeg_tune.SetPtEtaPhiM(b_recoMu_neg_tune_pt, b_recoMu_neg_tune_eta, b_recoMu_neg_tune_phi, 0.105658);
	    tLV_dimu_tune = tLV_recoMuonPos_tune + tLV_recoMuonNeg_tune;

	    b_recoDimu_tune     = true;
	    b_recoDimu_tune_pt  = tLV_dimu_tune.Pt();
	    b_recoDimu_tune_eta = tLV_dimu_tune.Eta();
	    b_recoDimu_tune_phi = tLV_dimu_tune.Phi();
	    b_recoDimu_tune_m   = tLV_dimu_tune.M();
	  } else {
	    b_recoDimu_tune     = false;
	    b_recoDimu_tune_pt  = -1.0;
	    b_recoDimu_tune_eta = 10.0;
	    b_recoDimu_tune_phi =  5.0;
	    b_recoDimu_tune_m   = -1.0;
	  }


      

	  if ( b_recoMu_pos_glb_pic == true && b_recoMu_neg_glb_pic == true ) {
	    TLorentzVector tLV_recoMuonPos_pic, tLV_recoMuonNeg_pic, tLV_dimu_pic;
	    tLV_recoMuonPos_pic.SetPtEtaPhiM(b_recoMu_pos_glb_pic_pt, b_recoMu_pos_glb_pic_eta, b_recoMu_pos_glb_pic_phi, 0.105658);
	    tLV_recoMuonNeg_pic.SetPtEtaPhiM(b_recoMu_neg_glb_pic_pt, b_recoMu_neg_glb_pic_eta, b_recoMu_neg_glb_pic_phi, 0.105658);
	    tLV_dimu_pic = tLV_recoMuonPos_pic + tLV_recoMuonNeg_pic;

	    b_recoDimu_glb_pic     = true;
	    b_recoDimu_glb_pic_pt  = tLV_dimu_pic.Pt();
	    b_recoDimu_glb_pic_eta = tLV_dimu_pic.Eta();
	    b_recoDimu_glb_pic_phi = tLV_dimu_pic.Phi();
	    b_recoDimu_glb_pic_m   = tLV_dimu_pic.M();
	  } else {
	    b_recoDimu_glb_pic     = false;
	    b_recoDimu_glb_pic_pt  = -1.0;
	    b_recoDimu_glb_pic_eta = 10.0;
	    b_recoDimu_glb_pic_phi =  5.0;
	    b_recoDimu_glb_pic_m   = -1.0;
	  }

	  if ( m_fillGenMuons ) {
	    if ( b_recoMu_pos_glb_gen == true && b_recoMu_neg_glb_gen == true ) {
		TLorentzVector tLV_recoMuonPos_glb_gen, tLV_recoMuonNeg_glb_gen, tLV_dimu_glb_gen;
		tLV_recoMuonPos_glb_gen.SetPtEtaPhiM(b_recoMu_pos_glb_gen_pt, b_recoMu_pos_glb_gen_eta, b_recoMu_pos_glb_gen_phi, 0.105658);
		tLV_recoMuonNeg_glb_gen.SetPtEtaPhiM(b_recoMu_neg_glb_gen_pt, b_recoMu_neg_glb_gen_eta, b_recoMu_neg_glb_gen_phi, 0.105658);
		tLV_dimu_glb_gen = tLV_recoMuonPos_glb_gen + tLV_recoMuonNeg_glb_gen;

		b_recoDimu_glb_gen     = true;
		b_recoDimu_glb_gen_pt  = tLV_dimu_glb_gen.Pt();
		b_recoDimu_glb_gen_eta = tLV_dimu_glb_gen.Eta();
		b_recoDimu_glb_gen_phi = tLV_dimu_glb_gen.Phi();
		b_recoDimu_glb_gen_m   = tLV_dimu_glb_gen.M();
	    } else {
		b_recoDimu_glb_gen     = false;
		b_recoDimu_glb_gen_pt  = -1.0;
		b_recoDimu_glb_gen_eta = 10.0;
		b_recoDimu_glb_gen_phi =  5.0;
		b_recoDimu_glb_gen_m   = -1.0;
	    }
	  }
	} else {
	  b_recoDimu_glb     = false;

	  b_recoDimu_glb_pt  = -1.0;
	  b_recoDimu_glb_eta = 10.0;
	  b_recoDimu_glb_phi =  5.0;
	  b_recoDimu_glb_m   = -1.0;

	  b_recoDimu_glb_trk_pt  = -1.0;
	  b_recoDimu_glb_trk_eta = 10.0;
	  b_recoDimu_glb_trk_phi =  5.0;
	  b_recoDimu_glb_trk_m   = -1.0;

	  b_recoDimu_glb_pic     = false;
	  b_recoDimu_glb_pic_pt  = -1.0;
	  b_recoDimu_glb_pic_eta = 10.0;
	  b_recoDimu_glb_pic_phi =  5.0;
	  b_recoDimu_glb_pic_m   = -1.0;

	  if ( m_fillGenMuons ) {
	    b_recoDimu_glb_gen     = false;
	    b_recoDimu_glb_gen_pt  = -1.0;
	    b_recoDimu_glb_gen_eta = 10.0;
	    b_recoDimu_glb_gen_phi =  5.0;
	    b_recoDimu_glb_gen_m   = -1.0;
	  }
	}

	if ( recoMuonPos->isStandAloneMuon() ) {
	  b_recoMu_pos_sta     = true;
	  b_recoMu_pos_sta_pt  = recoMuonPos->outerTrack()->pt();
	  b_recoMu_pos_sta_eta = recoMuonPos->outerTrack()->eta();
	  b_recoMu_pos_sta_phi = recoMuonPos->outerTrack()->phi();
	} else {
	  b_recoMu_pos_sta     = false;
	  b_recoMu_pos_sta_pt  = -1.0;
	  b_recoMu_pos_sta_eta = 10.0;
	  b_recoMu_pos_sta_phi =  5.0;
	}

	if ( recoMuonNeg->isStandAloneMuon() ) {
	  b_recoMu_neg_sta     = true;
	  b_recoMu_neg_sta_pt  = recoMuonNeg->outerTrack()->pt();
	  b_recoMu_neg_sta_eta = recoMuonNeg->outerTrack()->eta();
	  b_recoMu_neg_sta_phi = recoMuonNeg->outerTrack()->phi();
	} else {
	  b_recoMu_neg_sta     = -1.0;
	  b_recoMu_neg_sta_pt  =  5.0;
	  b_recoMu_neg_sta_eta = 10.0;
	  b_recoMu_neg_sta_phi = -1.0;
	}

	if ( b_recoMu_pos_sta == true && b_recoMu_neg_sta == true ) {
	  TLorentzVector tLV_recoMuonPos_sta, tLV_recoMuonNeg_sta, tLV_dimu_sta;
	  tLV_recoMuonPos_sta.SetPtEtaPhiM(b_recoMu_pos_sta_pt, b_recoMu_pos_sta_eta, b_recoMu_pos_sta_phi, 0.105658);
	  tLV_recoMuonNeg_sta.SetPtEtaPhiM(b_recoMu_neg_sta_pt, b_recoMu_neg_sta_eta, b_recoMu_neg_sta_phi, 0.105658);
	  tLV_dimu_sta = tLV_recoMuonPos_sta + tLV_recoMuonNeg_sta;

	  b_recoDimu_sta     = true;
	  b_recoDimu_sta_pt  = tLV_dimu_sta.Pt();
	  b_recoDimu_sta_eta = tLV_dimu_sta.Eta();
	  b_recoDimu_sta_phi = tLV_dimu_sta.Phi();
	  b_recoDimu_sta_m   = tLV_dimu_sta.M();

    if ( b_recoMu_pos_glb_pic == true && b_recoMu_neg_glb_pic == true ){
        randomInt =  random->Integer(2);
        TLorentzVector  tLV_dimu_hyb;
        b_recoDimu_hyb = true;
        TLorentzVector tLV_recoMuon_glb;
      
      

        if(randomInt > 0.5){
            tLV_recoMuon_glb.SetPtEtaPhiM(b_recoMu_pos_glb_pt, b_recoMu_pos_glb_eta, b_recoMu_pos_glb_phi, 0.105658);
            tLV_dimu_hyb = tLV_recoMuon_glb + tLV_recoMuonNeg_sta;
            b_recoDimu_hyb_sta_q = -1;
            b_recoDimu_hyb_sta_pt = b_recoMu_neg_sta_pt;
            b_recoDimu_hyb_sta_eta = b_recoMu_neg_sta_eta;
            b_recoDimu_hyb_sta_phi = b_recoMu_neg_sta_phi;

            b_recoDimu_hyb_glb_pt = b_recoMu_pos_glb_pt;
            b_recoDimu_hyb_glb_eta = b_recoMu_pos_glb_eta;
            b_recoDimu_hyb_glb_phi = b_recoMu_pos_glb_phi;
       } else {
            tLV_recoMuon_glb.SetPtEtaPhiM(b_recoMu_neg_glb_pt, b_recoMu_neg_glb_eta, b_recoMu_neg_glb_phi, 0.105658);
            tLV_dimu_hyb = tLV_recoMuon_glb + tLV_recoMuonPos_sta;
            b_recoDimu_hyb_sta_q = 1;
            b_recoDimu_hyb_sta_pt = b_recoMu_pos_sta_pt;
            b_recoDimu_hyb_sta_eta = b_recoMu_pos_sta_eta;
            b_recoDimu_hyb_sta_phi = b_recoMu_pos_sta_phi;

            b_recoDimu_hyb_glb_pt = b_recoMu_neg_glb_pt;
            b_recoDimu_hyb_glb_eta = b_recoMu_neg_glb_eta;
            b_recoDimu_hyb_glb_phi = b_recoMu_neg_glb_phi;
       }
            b_recoDimu_hyb_pt  = tLV_dimu_hyb.Pt();
            b_recoDimu_hyb_eta = tLV_dimu_hyb.Eta();
            b_recoDimu_hyb_phi = tLV_dimu_hyb.Phi();
            b_recoDimu_hyb_m = tLV_dimu_hyb.M();

      } else {
        b_recoDimu_hyb     = false;
        b_recoDimu_hyb_pt  = -1.0;
        b_recoDimu_hyb_eta = 10.0;
        b_recoDimu_hyb_phi =  5.0;
        b_recoDimu_hyb_sta_pt  = -1.0;
        b_recoDimu_hyb_sta_eta = 10.0;
        b_recoDimu_hyb_sta_phi =  5.0;

        b_recoDimu_hyb_glb_pt  = -1.0;
        b_recoDimu_hyb_glb_eta = 10.0;
        b_recoDimu_hyb_glb_phi =  5.0;

        b_recoDimu_hyb_m   = -1.0;
        b_recoDimu_hyb_sta_q   = 0.0;

      }



	} else {
	  b_recoDimu_sta     = false;
	  b_recoDimu_sta_pt  = -1.0;
	  b_recoDimu_sta_eta = 10.0;
	  b_recoDimu_sta_phi =  5.0;
	  b_recoDimu_sta_m   = -1.0;

      b_recoDimu_hyb     = false;
      b_recoDimu_hyb_pt  = -1.0;
      b_recoDimu_hyb_eta = 10.0;
      b_recoDimu_hyb_phi =  5.0;
      b_recoDimu_hyb_sta_pt  = -1.0;
      b_recoDimu_hyb_sta_eta = 10.0;
      b_recoDimu_hyb_sta_phi =  5.0;

      b_recoDimu_hyb_glb_pt  = -1.0;
      b_recoDimu_hyb_glb_eta = 10.0;
      b_recoDimu_hyb_glb_phi =  5.0;
      
      b_recoDimu_hyb_m   = -1.0;
      b_recoDimu_hyb_sta_q   = 0.0;


	}

	m_tree_recoDimuons->Fill();
    }
  }

  m_tree_events->Fill();

}


// ------------ method called once each job just before starting event loop  ------------
  void 
MuAlAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
  void 
MuAlAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
  void 
MuAlAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
  void 
MuAlAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
  void 
MuAlAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
  void 
MuAlAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MuAlAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MuAlAnalyzer);
