import ROOT
from DataFormats.FWLite import Events, Handle


rootList = [x[:-1] for x in open("test.txt")]
ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
outROOT = ROOT.TFile("CMSPOS.root","RECREATE")
cosmicMuonsModule,cosmicMuonsLabel,cosmicMuonsProcess, = "muons1Leg","",""
cosmicMuons= Handle("vector<reco::Muon>")
for i in rootList:
  print i
  events = Events(i)
  for e in events:
    e.getByLabel(cosmicMuonsModule,cosmicMuonsLabel,cosmicMuonsProcess, cosmicMuons)
    for mu in cosmicMuons.product():
      print mu.pt(), mu.eta(), mu.phi()

c = ROOT.TCanvas("","",800,600)
c.SaveAs("refitAnalyzer.png")


