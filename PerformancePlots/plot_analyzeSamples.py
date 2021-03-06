from ROOT import TLorentzVector
from random import randint
print >> sys.stderr, "Start analyze samples"

try:              threshold_pT_GeV
except NameError: threshold_pT_GeV = 30.0

iSample = -1

for sample in samples:
  iSample = iSample + 1
  print >> sys.stderr, "   Sample #", iSample
  filenames = sample[5:]
  for filename in filenames:
    print >> sys.stderr, "      Open file:", filename
    tfile = ROOT.TFile(filename)
    
    treeName = "muAlAnalyzer/Info"
    print >> sys.stderr, "      Read tree", treeName
    Info = tfile.Get(treeName)
    for info in Info:
      fillGenMuons    = False ##! info.fillGenMuons
      fillRecoMuons   = info.fillRecoMuons
      fillRecoDimuons = info.fillRecoDimuons
    
    print >> sys.stderr, "         fillGenMuons = ",    fillGenMuons
    print >> sys.stderr, "         fillRecoMuons = ",   fillRecoMuons
    print >> sys.stderr, "         fillRecoDimuons = ", fillRecoDimuons
    
    if ( fillRecoMuons ):
      counterRecoMuons = 0 # reset counter for every file
      treeName = "muAlAnalyzer/recoMuons"
      print >> sys.stderr, "      Read tree", treeName
      recoMuons = tfile.Get(treeName)
      print >> sys.stderr, "         Total number of entries in the tree:", recoMuons.GetEntriesFast()
      
      for mu in recoMuons:
        if maxEntries > 0 and counterRecoMuons >= maxEntries:
          break
        if ( not counterRecoMuons%10000 ):
          print >> sys.stderr, counterRecoMuons
        counterRecoMuons = counterRecoMuons + 1
        if ( mu.glb ):
          h_glb_pt[iSample].Fill(mu.glb_pt)
          h_glb_nchi2[iSample].Fill(mu.glb_nchi2)
          if abs(mu.glb_eta) < 0.9 :
            h_glb_nchi2_bar[iSample].Fill(mu.glb_nchi2)
          if abs(mu.glb_eta) > 1.2 :
            h_glb_nchi2_csc[iSample].Fill(mu.glb_nchi2)
          h_glb_eta[iSample].Fill(mu.glb_eta)
          h_glb_phi[iSample].Fill(mu.glb_phi)
          
          h_glb_trk_pt[iSample].Fill(mu.glb_trk_pt)
#          h_glb_trk_nchi2[iSample].Fill(mu.glb_trk_nchi2)
          h_glb_trk_eta[iSample].Fill(mu.glb_trk_eta)
          h_glb_trk_phi[iSample].Fill(mu.glb_trk_phi)
          
          if ( mu.glb_pic ):
            h_glb_pic_pt[iSample].Fill(mu.glb_pic_pt)
#            h_glb_pic_nchi2[iSample].Fill(mu.glb_pic_nchi2)
            h_glb_pic_eta[iSample].Fill(mu.glb_pic_eta)
            h_glb_pic_phi[iSample].Fill(mu.glb_pic_phi)
          
        if ( mu.sta ):
          h_sta_pt[iSample].Fill(mu.sta_pt)
          h_sta_nchi2[iSample].Fill(mu.sta_nchi2)
          if abs(mu.sta_eta) < 0.9 :
            h_sta_nchi2_bar[iSample].Fill(mu.sta_nchi2)     
          if abs(mu.sta_eta) > 1.2 :
            h_sta_nchi2_csc[iSample].Fill(mu.sta_nchi2)
          h_sta_eta[iSample].Fill(mu.sta_eta)
          h_sta_phi[iSample].Fill(mu.sta_phi)
        
        # pT resolution for STA muons w.r.t. GLB muons
        if ( mu.sta and mu.glb and mu.glb_trk_pt > threshold_pT_GeV):
          if ( mu.sta_pt != 0.0 and mu.glb_pt != 0.0 ):
            ptRes_sta_glb = mu.q/mu.sta_pt - mu.q/mu.glb_pt
            h_ptRes_sta_glb[iSample].Fill(ptRes_sta_glb)
            # resolution vs eta
            if ( mu.glb_eta >= -2.4 and mu.glb_eta <= -2.1 ): h_ptRes_sta_glb_eta_m24_m21[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >= -2.1 and mu.glb_eta <= -1.8 ): h_ptRes_sta_glb_eta_m21_m18[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >= -1.8 and mu.glb_eta <= -1.5 ): h_ptRes_sta_glb_eta_m18_m15[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >= -1.5 and mu.glb_eta <= -1.2 ): h_ptRes_sta_glb_eta_m15_m12[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >= -1.2 and mu.glb_eta <= -0.9 ): h_ptRes_sta_glb_eta_m12_m09[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >= -0.9 and mu.glb_eta <= -0.6 ): h_ptRes_sta_glb_eta_m09_m06[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >= -0.6 and mu.glb_eta <= -0.3 ): h_ptRes_sta_glb_eta_m06_m03[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >= -0.3 and mu.glb_eta <=  0.0 ): h_ptRes_sta_glb_eta_m03_m00[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  0.0 and mu.glb_eta <=  0.3 ): h_ptRes_sta_glb_eta_p00_p03[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  0.3 and mu.glb_eta <=  0.6 ): h_ptRes_sta_glb_eta_p03_p06[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  0.6 and mu.glb_eta <=  0.9 ): h_ptRes_sta_glb_eta_p06_p09[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  0.9 and mu.glb_eta <=  1.2 ): h_ptRes_sta_glb_eta_p09_p12[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  1.2 and mu.glb_eta <=  1.5 ): h_ptRes_sta_glb_eta_p12_p15[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  1.5 and mu.glb_eta <=  1.8 ): h_ptRes_sta_glb_eta_p15_p18[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  1.8 and mu.glb_eta <=  2.1 ): h_ptRes_sta_glb_eta_p18_p21[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  2.1 and mu.glb_eta <=  2.4 ): h_ptRes_sta_glb_eta_p21_p24[iSample].Fill(ptRes_sta_glb)
            # resolution vs phi
            if ( mu.glb_phi >= -3.2 and mu.glb_phi <= -2.8 ): h_ptRes_sta_glb_phi_m32_m28[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >= -2.8 and mu.glb_phi <= -2.4 ): h_ptRes_sta_glb_phi_m28_m24[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >= -2.4 and mu.glb_phi <= -2.0 ): h_ptRes_sta_glb_phi_m24_m20[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >= -2.0 and mu.glb_phi <= -1.6 ): h_ptRes_sta_glb_phi_m20_m16[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >= -1.6 and mu.glb_phi <= -1.2 ): h_ptRes_sta_glb_phi_m16_m12[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >= -1.2 and mu.glb_phi <= -0.8 ): h_ptRes_sta_glb_phi_m12_m08[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >= -0.8 and mu.glb_phi <= -0.4 ): h_ptRes_sta_glb_phi_m08_m04[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >= -0.4 and mu.glb_phi <=  0.0 ): h_ptRes_sta_glb_phi_m04_m00[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >=  0.0 and mu.glb_phi <=  0.4 ): h_ptRes_sta_glb_phi_p00_p04[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >=  0.4 and mu.glb_phi <=  0.8 ): h_ptRes_sta_glb_phi_p04_p08[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >=  0.8 and mu.glb_phi <=  1.2 ): h_ptRes_sta_glb_phi_p08_p12[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >=  1.2 and mu.glb_phi <=  1.6 ): h_ptRes_sta_glb_phi_p12_p16[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >=  1.6 and mu.glb_phi <=  2.0 ): h_ptRes_sta_glb_phi_p16_p20[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >=  2.0 and mu.glb_phi <=  2.4 ): h_ptRes_sta_glb_phi_p20_p24[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >=  2.4 and mu.glb_phi <=  2.8 ): h_ptRes_sta_glb_phi_p24_p28[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_phi >=  2.8 and mu.glb_phi <=  3.2 ): h_ptRes_sta_glb_phi_p28_p32[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  -0.9 and mu.glb_eta <=  0.9 ): 
              if ( mu.glb_phi >= -3.2 and mu.glb_phi <= -2.8 ): h_ptRes_sta_glbB_phi_m32_m28[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.8 and mu.glb_phi <= -2.4 ): h_ptRes_sta_glbB_phi_m28_m24[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.4 and mu.glb_phi <= -2.0 ): h_ptRes_sta_glbB_phi_m24_m20[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.0 and mu.glb_phi <= -1.6 ): h_ptRes_sta_glbB_phi_m20_m16[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -1.6 and mu.glb_phi <= -1.2 ): h_ptRes_sta_glbB_phi_m16_m12[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -1.2 and mu.glb_phi <= -0.8 ): h_ptRes_sta_glbB_phi_m12_m08[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -0.8 and mu.glb_phi <= -0.4 ): h_ptRes_sta_glbB_phi_m08_m04[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -0.4 and mu.glb_phi <=  0.0 ): h_ptRes_sta_glbB_phi_m04_m00[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.0 and mu.glb_phi <=  0.4 ): h_ptRes_sta_glbB_phi_p00_p04[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.4 and mu.glb_phi <=  0.8 ): h_ptRes_sta_glbB_phi_p04_p08[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.8 and mu.glb_phi <=  1.2 ): h_ptRes_sta_glbB_phi_p08_p12[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  1.2 and mu.glb_phi <=  1.6 ): h_ptRes_sta_glbB_phi_p12_p16[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  1.6 and mu.glb_phi <=  2.0 ): h_ptRes_sta_glbB_phi_p16_p20[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.0 and mu.glb_phi <=  2.4 ): h_ptRes_sta_glbB_phi_p20_p24[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.4 and mu.glb_phi <=  2.8 ): h_ptRes_sta_glbB_phi_p24_p28[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.8 and mu.glb_phi <=  3.2 ): h_ptRes_sta_glbB_phi_p28_p32[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  0.9 and mu.glb_eta <=  2.4 ): 
              if ( mu.glb_phi >= -3.2 and mu.glb_phi <= -2.8 ): h_ptRes_sta_glbEOp_phi_m32_m28[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.8 and mu.glb_phi <= -2.4 ): h_ptRes_sta_glbEOp_phi_m28_m24[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.4 and mu.glb_phi <= -2.0 ): h_ptRes_sta_glbEOp_phi_m24_m20[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.0 and mu.glb_phi <= -1.6 ): h_ptRes_sta_glbEOp_phi_m20_m16[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -1.6 and mu.glb_phi <= -1.2 ): h_ptRes_sta_glbEOp_phi_m16_m12[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -1.2 and mu.glb_phi <= -0.8 ): h_ptRes_sta_glbEOp_phi_m12_m08[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -0.8 and mu.glb_phi <= -0.4 ): h_ptRes_sta_glbEOp_phi_m08_m04[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -0.4 and mu.glb_phi <=  0.0 ): h_ptRes_sta_glbEOp_phi_m04_m00[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.0 and mu.glb_phi <=  0.4 ): h_ptRes_sta_glbEOp_phi_p00_p04[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.4 and mu.glb_phi <=  0.8 ): h_ptRes_sta_glbEOp_phi_p04_p08[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.8 and mu.glb_phi <=  1.2 ): h_ptRes_sta_glbEOp_phi_p08_p12[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  1.2 and mu.glb_phi <=  1.6 ): h_ptRes_sta_glbEOp_phi_p12_p16[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  1.6 and mu.glb_phi <=  2.0 ): h_ptRes_sta_glbEOp_phi_p16_p20[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.0 and mu.glb_phi <=  2.4 ): h_ptRes_sta_glbEOp_phi_p20_p24[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.4 and mu.glb_phi <=  2.8 ): h_ptRes_sta_glbEOp_phi_p24_p28[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.8 and mu.glb_phi <=  3.2 ): h_ptRes_sta_glbEOp_phi_p28_p32[iSample].Fill(ptRes_sta_glb)
            if ( mu.glb_eta >=  -2.4 and mu.glb_eta <=  -0.9 ): 
              if ( mu.glb_phi >= -3.2 and mu.glb_phi <= -2.8 ): h_ptRes_sta_glbEOm_phi_m32_m28[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.8 and mu.glb_phi <= -2.4 ): h_ptRes_sta_glbEOm_phi_m28_m24[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.4 and mu.glb_phi <= -2.0 ): h_ptRes_sta_glbEOm_phi_m24_m20[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -2.0 and mu.glb_phi <= -1.6 ): h_ptRes_sta_glbEOm_phi_m20_m16[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -1.6 and mu.glb_phi <= -1.2 ): h_ptRes_sta_glbEOm_phi_m16_m12[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -1.2 and mu.glb_phi <= -0.8 ): h_ptRes_sta_glbEOm_phi_m12_m08[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -0.8 and mu.glb_phi <= -0.4 ): h_ptRes_sta_glbEOm_phi_m08_m04[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >= -0.4 and mu.glb_phi <=  0.0 ): h_ptRes_sta_glbEOm_phi_m04_m00[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.0 and mu.glb_phi <=  0.4 ): h_ptRes_sta_glbEOm_phi_p00_p04[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.4 and mu.glb_phi <=  0.8 ): h_ptRes_sta_glbEOm_phi_p04_p08[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  0.8 and mu.glb_phi <=  1.2 ): h_ptRes_sta_glbEOm_phi_p08_p12[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  1.2 and mu.glb_phi <=  1.6 ): h_ptRes_sta_glbEOm_phi_p12_p16[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  1.6 and mu.glb_phi <=  2.0 ): h_ptRes_sta_glbEOm_phi_p16_p20[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.0 and mu.glb_phi <=  2.4 ): h_ptRes_sta_glbEOm_phi_p20_p24[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.4 and mu.glb_phi <=  2.8 ): h_ptRes_sta_glbEOm_phi_p24_p28[iSample].Fill(ptRes_sta_glb)
              if ( mu.glb_phi >=  2.8 and mu.glb_phi <=  3.2 ): h_ptRes_sta_glbEOm_phi_p28_p32[iSample].Fill(ptRes_sta_glb)
        
        # pT resolution STA muons w.r.t. GEN muons matched to GLB muons
        if ( fillGenMuons and mu.sta and mu.glb and mu.glb_gen_pt > threshold_pT_GeV ):
          if ( mu.sta_pt != 0.0 and mu.glb_gen_pt != 0.0 ):
            ptRes_sta_glb_gen = mu.q/mu.sta_pt - mu.q/mu.glb_gen_pt
            h_ptRes_sta_glb_gen[iSample].Fill(ptRes_sta_glb_gen)
            # resolution vs eta
            if ( mu.glb_gen_eta >= -2.4 and mu.glb_gen_eta <= -2.1 ): h_ptRes_sta_glb_gen_eta_m24_m21[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >= -2.1 and mu.glb_gen_eta <= -1.8 ): h_ptRes_sta_glb_gen_eta_m21_m18[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >= -1.8 and mu.glb_gen_eta <= -1.5 ): h_ptRes_sta_glb_gen_eta_m18_m15[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >= -1.5 and mu.glb_gen_eta <= -1.2 ): h_ptRes_sta_glb_gen_eta_m15_m12[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >= -1.2 and mu.glb_gen_eta <= -0.9 ): h_ptRes_sta_glb_gen_eta_m12_m09[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >= -0.9 and mu.glb_gen_eta <= -0.6 ): h_ptRes_sta_glb_gen_eta_m09_m06[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >= -0.6 and mu.glb_gen_eta <= -0.3 ): h_ptRes_sta_glb_gen_eta_m06_m03[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >= -0.3 and mu.glb_gen_eta <=  0.0 ): h_ptRes_sta_glb_gen_eta_m03_m00[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  0.0 and mu.glb_gen_eta <=  0.3 ): h_ptRes_sta_glb_gen_eta_p00_p03[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  0.3 and mu.glb_gen_eta <=  0.6 ): h_ptRes_sta_glb_gen_eta_p03_p06[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  0.6 and mu.glb_gen_eta <=  0.9 ): h_ptRes_sta_glb_gen_eta_p06_p09[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  0.9 and mu.glb_gen_eta <=  1.2 ): h_ptRes_sta_glb_gen_eta_p09_p12[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  1.2 and mu.glb_gen_eta <=  1.5 ): h_ptRes_sta_glb_gen_eta_p12_p15[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  1.5 and mu.glb_gen_eta <=  1.8 ): h_ptRes_sta_glb_gen_eta_p15_p18[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  1.8 and mu.glb_gen_eta <=  2.1 ): h_ptRes_sta_glb_gen_eta_p18_p21[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  2.1 and mu.glb_gen_eta <=  2.4 ): h_ptRes_sta_glb_gen_eta_p21_p24[iSample].Fill(ptRes_sta_glb_gen)
            # resolution vs phi
            if ( mu.glb_gen_phi >= -3.2 and mu.glb_gen_phi <= -2.8 ): h_ptRes_sta_glb_gen_phi_m32_m28[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >= -2.8 and mu.glb_gen_phi <= -2.4 ): h_ptRes_sta_glb_gen_phi_m28_m24[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >= -2.4 and mu.glb_gen_phi <= -2.0 ): h_ptRes_sta_glb_gen_phi_m24_m20[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >= -2.0 and mu.glb_gen_phi <= -1.6 ): h_ptRes_sta_glb_gen_phi_m20_m16[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >= -1.6 and mu.glb_gen_phi <= -1.2 ): h_ptRes_sta_glb_gen_phi_m16_m12[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >= -1.2 and mu.glb_gen_phi <= -0.8 ): h_ptRes_sta_glb_gen_phi_m12_m08[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >= -0.8 and mu.glb_gen_phi <= -0.4 ): h_ptRes_sta_glb_gen_phi_m08_m04[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >= -0.4 and mu.glb_gen_phi <=  0.0 ): h_ptRes_sta_glb_gen_phi_m04_m00[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >=  0.0 and mu.glb_gen_phi <=  0.4 ): h_ptRes_sta_glb_gen_phi_p00_p04[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >=  0.4 and mu.glb_gen_phi <=  0.8 ): h_ptRes_sta_glb_gen_phi_p04_p08[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >=  0.8 and mu.glb_gen_phi <=  1.2 ): h_ptRes_sta_glb_gen_phi_p08_p12[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >=  1.2 and mu.glb_gen_phi <=  1.6 ): h_ptRes_sta_glb_gen_phi_p12_p16[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >=  1.6 and mu.glb_gen_phi <=  2.0 ): h_ptRes_sta_glb_gen_phi_p16_p20[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >=  2.0 and mu.glb_gen_phi <=  2.4 ): h_ptRes_sta_glb_gen_phi_p20_p24[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >=  2.4 and mu.glb_gen_phi <=  2.8 ): h_ptRes_sta_glb_gen_phi_p24_p28[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_phi >=  2.8 and mu.glb_gen_phi <=  3.2 ): h_ptRes_sta_glb_gen_phi_p28_p32[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  -0.9 and mu.glb_gen_eta <=  0.9 ): 
              if ( mu.glb_gen_phi >= -3.2 and mu.glb_gen_phi <= -2.8 ): h_ptRes_sta_glb_genB_phi_m32_m28[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.8 and mu.glb_gen_phi <= -2.4 ): h_ptRes_sta_glb_genB_phi_m28_m24[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.4 and mu.glb_gen_phi <= -2.0 ): h_ptRes_sta_glb_genB_phi_m24_m20[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.0 and mu.glb_gen_phi <= -1.6 ): h_ptRes_sta_glb_genB_phi_m20_m16[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -1.6 and mu.glb_gen_phi <= -1.2 ): h_ptRes_sta_glb_genB_phi_m16_m12[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -1.2 and mu.glb_gen_phi <= -0.8 ): h_ptRes_sta_glb_genB_phi_m12_m08[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -0.8 and mu.glb_gen_phi <= -0.4 ): h_ptRes_sta_glb_genB_phi_m08_m04[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -0.4 and mu.glb_gen_phi <=  0.0 ): h_ptRes_sta_glb_genB_phi_m04_m00[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.0 and mu.glb_gen_phi <=  0.4 ): h_ptRes_sta_glb_genB_phi_p00_p04[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.4 and mu.glb_gen_phi <=  0.8 ): h_ptRes_sta_glb_genB_phi_p04_p08[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.8 and mu.glb_gen_phi <=  1.2 ): h_ptRes_sta_glb_genB_phi_p08_p12[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  1.2 and mu.glb_gen_phi <=  1.6 ): h_ptRes_sta_glb_genB_phi_p12_p16[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  1.6 and mu.glb_gen_phi <=  2.0 ): h_ptRes_sta_glb_genB_phi_p16_p20[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.0 and mu.glb_gen_phi <=  2.4 ): h_ptRes_sta_glb_genB_phi_p20_p24[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.4 and mu.glb_gen_phi <=  2.8 ): h_ptRes_sta_glb_genB_phi_p24_p28[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.8 and mu.glb_gen_phi <=  3.2 ): h_ptRes_sta_glb_genB_phi_p28_p32[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  0.9 and mu.glb_gen_eta <=  2.4 ): 
              if ( mu.glb_gen_phi >= -3.2 and mu.glb_gen_phi <= -2.8 ): h_ptRes_sta_glb_genEOp_phi_m32_m28[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.8 and mu.glb_gen_phi <= -2.4 ): h_ptRes_sta_glb_genEOp_phi_m28_m24[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.4 and mu.glb_gen_phi <= -2.0 ): h_ptRes_sta_glb_genEOp_phi_m24_m20[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.0 and mu.glb_gen_phi <= -1.6 ): h_ptRes_sta_glb_genEOp_phi_m20_m16[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -1.6 and mu.glb_gen_phi <= -1.2 ): h_ptRes_sta_glb_genEOp_phi_m16_m12[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -1.2 and mu.glb_gen_phi <= -0.8 ): h_ptRes_sta_glb_genEOp_phi_m12_m08[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -0.8 and mu.glb_gen_phi <= -0.4 ): h_ptRes_sta_glb_genEOp_phi_m08_m04[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -0.4 and mu.glb_gen_phi <=  0.0 ): h_ptRes_sta_glb_genEOp_phi_m04_m00[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.0 and mu.glb_gen_phi <=  0.4 ): h_ptRes_sta_glb_genEOp_phi_p00_p04[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.4 and mu.glb_gen_phi <=  0.8 ): h_ptRes_sta_glb_genEOp_phi_p04_p08[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.8 and mu.glb_gen_phi <=  1.2 ): h_ptRes_sta_glb_genEOp_phi_p08_p12[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  1.2 and mu.glb_gen_phi <=  1.6 ): h_ptRes_sta_glb_genEOp_phi_p12_p16[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  1.6 and mu.glb_gen_phi <=  2.0 ): h_ptRes_sta_glb_genEOp_phi_p16_p20[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.0 and mu.glb_gen_phi <=  2.4 ): h_ptRes_sta_glb_genEOp_phi_p20_p24[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.4 and mu.glb_gen_phi <=  2.8 ): h_ptRes_sta_glb_genEOp_phi_p24_p28[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.8 and mu.glb_gen_phi <=  3.2 ): h_ptRes_sta_glb_genEOp_phi_p28_p32[iSample].Fill(ptRes_sta_glb_gen)
            if ( mu.glb_gen_eta >=  -2.4 and mu.glb_gen_eta <=  -0.9 ): 
              if ( mu.glb_gen_phi >= -3.2 and mu.glb_gen_phi <= -2.8 ): h_ptRes_sta_glb_genEOm_phi_m32_m28[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.8 and mu.glb_gen_phi <= -2.4 ): h_ptRes_sta_glb_genEOm_phi_m28_m24[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.4 and mu.glb_gen_phi <= -2.0 ): h_ptRes_sta_glb_genEOm_phi_m24_m20[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -2.0 and mu.glb_gen_phi <= -1.6 ): h_ptRes_sta_glb_genEOm_phi_m20_m16[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -1.6 and mu.glb_gen_phi <= -1.2 ): h_ptRes_sta_glb_genEOm_phi_m16_m12[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -1.2 and mu.glb_gen_phi <= -0.8 ): h_ptRes_sta_glb_genEOm_phi_m12_m08[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -0.8 and mu.glb_gen_phi <= -0.4 ): h_ptRes_sta_glb_genEOm_phi_m08_m04[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >= -0.4 and mu.glb_gen_phi <=  0.0 ): h_ptRes_sta_glb_genEOm_phi_m04_m00[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.0 and mu.glb_gen_phi <=  0.4 ): h_ptRes_sta_glb_genEOm_phi_p00_p04[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.4 and mu.glb_gen_phi <=  0.8 ): h_ptRes_sta_glb_genEOm_phi_p04_p08[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  0.8 and mu.glb_gen_phi <=  1.2 ): h_ptRes_sta_glb_genEOm_phi_p08_p12[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  1.2 and mu.glb_gen_phi <=  1.6 ): h_ptRes_sta_glb_genEOm_phi_p12_p16[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  1.6 and mu.glb_gen_phi <=  2.0 ): h_ptRes_sta_glb_genEOm_phi_p16_p20[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.0 and mu.glb_gen_phi <=  2.4 ): h_ptRes_sta_glb_genEOm_phi_p20_p24[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.4 and mu.glb_gen_phi <=  2.8 ): h_ptRes_sta_glb_genEOm_phi_p24_p28[iSample].Fill(ptRes_sta_glb_gen)
              if ( mu.glb_gen_phi >=  2.8 and mu.glb_gen_phi <=  3.2 ): h_ptRes_sta_glb_genEOm_phi_p28_p32[iSample].Fill(ptRes_sta_glb_gen)
        
        # pT resolution of GLB Picky muons w.r.t. GLB muons (tracker part only)
        if ( mu.glb_pic and mu.glb_trk_pt > threshold_pT_GeV):
          if ( mu.glb_pic_pt != 0.0 and mu.glb_trk_pt != 0.0 ):
            ptRes_pic_trk = mu.q/mu.glb_pic_pt - mu.q/mu.glb_trk_pt
            h_ptRes_pic_trk[iSample].Fill(ptRes_pic_trk)
            # resolution vs eta
            if ( mu.glb_trk_eta >= -2.4 and mu.glb_trk_eta <= -2.1 ): h_ptRes_pic_trk_eta_m24_m21[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >= -2.1 and mu.glb_trk_eta <= -1.8 ): h_ptRes_pic_trk_eta_m21_m18[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >= -1.8 and mu.glb_trk_eta <= -1.5 ): h_ptRes_pic_trk_eta_m18_m15[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >= -1.5 and mu.glb_trk_eta <= -1.2 ): h_ptRes_pic_trk_eta_m15_m12[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >= -1.2 and mu.glb_trk_eta <= -0.9 ): h_ptRes_pic_trk_eta_m12_m09[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >= -0.9 and mu.glb_trk_eta <= -0.6 ): h_ptRes_pic_trk_eta_m09_m06[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >= -0.6 and mu.glb_trk_eta <= -0.3 ): h_ptRes_pic_trk_eta_m06_m03[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >= -0.3 and mu.glb_trk_eta <=  0.0 ): h_ptRes_pic_trk_eta_m03_m00[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  0.0 and mu.glb_trk_eta <=  0.3 ): h_ptRes_pic_trk_eta_p00_p03[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  0.3 and mu.glb_trk_eta <=  0.6 ): h_ptRes_pic_trk_eta_p03_p06[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  0.6 and mu.glb_trk_eta <=  0.9 ): h_ptRes_pic_trk_eta_p06_p09[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  0.9 and mu.glb_trk_eta <=  1.2 ): h_ptRes_pic_trk_eta_p09_p12[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  1.2 and mu.glb_trk_eta <=  1.5 ): h_ptRes_pic_trk_eta_p12_p15[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  1.5 and mu.glb_trk_eta <=  1.8 ): h_ptRes_pic_trk_eta_p15_p18[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  1.8 and mu.glb_trk_eta <=  2.1 ): h_ptRes_pic_trk_eta_p18_p21[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  2.1 and mu.glb_trk_eta <=  2.4 ): h_ptRes_pic_trk_eta_p21_p24[iSample].Fill(ptRes_pic_trk)
            # resolution vs phi
            if ( mu.glb_trk_phi >= -3.2 and mu.glb_trk_phi <= -2.8 ): h_ptRes_pic_trk_phi_m32_m28[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >= -2.8 and mu.glb_trk_phi <= -2.4 ): h_ptRes_pic_trk_phi_m28_m24[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >= -2.4 and mu.glb_trk_phi <= -2.0 ): h_ptRes_pic_trk_phi_m24_m20[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >= -2.0 and mu.glb_trk_phi <= -1.6 ): h_ptRes_pic_trk_phi_m20_m16[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >= -1.6 and mu.glb_trk_phi <= -1.2 ): h_ptRes_pic_trk_phi_m16_m12[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >= -1.2 and mu.glb_trk_phi <= -0.8 ): h_ptRes_pic_trk_phi_m12_m08[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >= -0.8 and mu.glb_trk_phi <= -0.4 ): h_ptRes_pic_trk_phi_m08_m04[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >= -0.4 and mu.glb_trk_phi <=  0.0 ): h_ptRes_pic_trk_phi_m04_m00[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >=  0.0 and mu.glb_trk_phi <=  0.4 ): h_ptRes_pic_trk_phi_p00_p04[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >=  0.4 and mu.glb_trk_phi <=  0.8 ): h_ptRes_pic_trk_phi_p04_p08[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >=  0.8 and mu.glb_trk_phi <=  1.2 ): h_ptRes_pic_trk_phi_p08_p12[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >=  1.2 and mu.glb_trk_phi <=  1.6 ): h_ptRes_pic_trk_phi_p12_p16[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >=  1.6 and mu.glb_trk_phi <=  2.0 ): h_ptRes_pic_trk_phi_p16_p20[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >=  2.0 and mu.glb_trk_phi <=  2.4 ): h_ptRes_pic_trk_phi_p20_p24[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >=  2.4 and mu.glb_trk_phi <=  2.8 ): h_ptRes_pic_trk_phi_p24_p28[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_phi >=  2.8 and mu.glb_trk_phi <=  3.2 ): h_ptRes_pic_trk_phi_p28_p32[iSample].Fill(ptRes_pic_trk)
            
            if ( mu.glb_trk_eta >=  -0.9 and mu.glb_trk_eta <=  0.9 ): 
              if ( mu.glb_trk_phi >= -3.2 and mu.glb_trk_phi <= -2.8 ): h_ptRes_pic_trkB_phi_m32_m28[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.8 and mu.glb_trk_phi <= -2.4 ): h_ptRes_pic_trkB_phi_m28_m24[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.4 and mu.glb_trk_phi <= -2.0 ): h_ptRes_pic_trkB_phi_m24_m20[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.0 and mu.glb_trk_phi <= -1.6 ): h_ptRes_pic_trkB_phi_m20_m16[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -1.6 and mu.glb_trk_phi <= -1.2 ): h_ptRes_pic_trkB_phi_m16_m12[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -1.2 and mu.glb_trk_phi <= -0.8 ): h_ptRes_pic_trkB_phi_m12_m08[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -0.8 and mu.glb_trk_phi <= -0.4 ): h_ptRes_pic_trkB_phi_m08_m04[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -0.4 and mu.glb_trk_phi <=  0.0 ): h_ptRes_pic_trkB_phi_m04_m00[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.0 and mu.glb_trk_phi <=  0.4 ): h_ptRes_pic_trkB_phi_p00_p04[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.4 and mu.glb_trk_phi <=  0.8 ): h_ptRes_pic_trkB_phi_p04_p08[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.8 and mu.glb_trk_phi <=  1.2 ): h_ptRes_pic_trkB_phi_p08_p12[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  1.2 and mu.glb_trk_phi <=  1.6 ): h_ptRes_pic_trkB_phi_p12_p16[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  1.6 and mu.glb_trk_phi <=  2.0 ): h_ptRes_pic_trkB_phi_p16_p20[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.0 and mu.glb_trk_phi <=  2.4 ): h_ptRes_pic_trkB_phi_p20_p24[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.4 and mu.glb_trk_phi <=  2.8 ): h_ptRes_pic_trkB_phi_p24_p28[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.8 and mu.glb_trk_phi <=  3.2 ): h_ptRes_pic_trkB_phi_p28_p32[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  0.9 and mu.glb_trk_eta <=  2.4 ): 
              if ( mu.glb_trk_phi >= -3.2 and mu.glb_trk_phi <= -2.8 ): h_ptRes_pic_trkEOp_phi_m32_m28[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.8 and mu.glb_trk_phi <= -2.4 ): h_ptRes_pic_trkEOp_phi_m28_m24[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.4 and mu.glb_trk_phi <= -2.0 ): h_ptRes_pic_trkEOp_phi_m24_m20[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.0 and mu.glb_trk_phi <= -1.6 ): h_ptRes_pic_trkEOp_phi_m20_m16[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -1.6 and mu.glb_trk_phi <= -1.2 ): h_ptRes_pic_trkEOp_phi_m16_m12[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -1.2 and mu.glb_trk_phi <= -0.8 ): h_ptRes_pic_trkEOp_phi_m12_m08[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -0.8 and mu.glb_trk_phi <= -0.4 ): h_ptRes_pic_trkEOp_phi_m08_m04[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -0.4 and mu.glb_trk_phi <=  0.0 ): h_ptRes_pic_trkEOp_phi_m04_m00[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.0 and mu.glb_trk_phi <=  0.4 ): h_ptRes_pic_trkEOp_phi_p00_p04[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.4 and mu.glb_trk_phi <=  0.8 ): h_ptRes_pic_trkEOp_phi_p04_p08[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.8 and mu.glb_trk_phi <=  1.2 ): h_ptRes_pic_trkEOp_phi_p08_p12[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  1.2 and mu.glb_trk_phi <=  1.6 ): h_ptRes_pic_trkEOp_phi_p12_p16[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  1.6 and mu.glb_trk_phi <=  2.0 ): h_ptRes_pic_trkEOp_phi_p16_p20[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.0 and mu.glb_trk_phi <=  2.4 ): h_ptRes_pic_trkEOp_phi_p20_p24[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.4 and mu.glb_trk_phi <=  2.8 ): h_ptRes_pic_trkEOp_phi_p24_p28[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.8 and mu.glb_trk_phi <=  3.2 ): h_ptRes_pic_trkEOp_phi_p28_p32[iSample].Fill(ptRes_pic_trk)
            if ( mu.glb_trk_eta >=  -2.4 and mu.glb_trk_eta <=  -0.9 ): 
              if ( mu.glb_trk_phi >= -3.2 and mu.glb_trk_phi <= -2.8 ): h_ptRes_pic_trkEOm_phi_m32_m28[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.8 and mu.glb_trk_phi <= -2.4 ): h_ptRes_pic_trkEOm_phi_m28_m24[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.4 and mu.glb_trk_phi <= -2.0 ): h_ptRes_pic_trkEOm_phi_m24_m20[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -2.0 and mu.glb_trk_phi <= -1.6 ): h_ptRes_pic_trkEOm_phi_m20_m16[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -1.6 and mu.glb_trk_phi <= -1.2 ): h_ptRes_pic_trkEOm_phi_m16_m12[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -1.2 and mu.glb_trk_phi <= -0.8 ): h_ptRes_pic_trkEOm_phi_m12_m08[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -0.8 and mu.glb_trk_phi <= -0.4 ): h_ptRes_pic_trkEOm_phi_m08_m04[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >= -0.4 and mu.glb_trk_phi <=  0.0 ): h_ptRes_pic_trkEOm_phi_m04_m00[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.0 and mu.glb_trk_phi <=  0.4 ): h_ptRes_pic_trkEOm_phi_p00_p04[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.4 and mu.glb_trk_phi <=  0.8 ): h_ptRes_pic_trkEOm_phi_p04_p08[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  0.8 and mu.glb_trk_phi <=  1.2 ): h_ptRes_pic_trkEOm_phi_p08_p12[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  1.2 and mu.glb_trk_phi <=  1.6 ): h_ptRes_pic_trkEOm_phi_p12_p16[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  1.6 and mu.glb_trk_phi <=  2.0 ): h_ptRes_pic_trkEOm_phi_p16_p20[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.0 and mu.glb_trk_phi <=  2.4 ): h_ptRes_pic_trkEOm_phi_p20_p24[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.4 and mu.glb_trk_phi <=  2.8 ): h_ptRes_pic_trkEOm_phi_p24_p28[iSample].Fill(ptRes_pic_trk)
              if ( mu.glb_trk_phi >=  2.8 and mu.glb_trk_phi <=  3.2 ): h_ptRes_pic_trkEOm_phi_p28_p32[iSample].Fill(ptRes_pic_trk)
        
        # pT resolution of GLB Picky muons w.r.t. GEN muons matched to the GLB muons
        if ( fillGenMuons and mu.glb_pic and mu.glb_gen_pt > threshold_pT_GeV ):
          if ( mu.glb_pic_pt != 0.0 and mu.glb_gen_pt != 0.0 ):
            ptRes_pic_gen = mu.q/mu.glb_pic_pt - mu.q/mu.glb_gen_pt
            h_ptRes_pic_gen[iSample].Fill(ptRes_pic_gen)
            # resolution vs eta
            if ( mu.glb_gen_eta >= -2.4 and mu.glb_gen_eta <= -2.1 ): h_ptRes_pic_gen_eta_m24_m21[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >= -2.1 and mu.glb_gen_eta <= -1.8 ): h_ptRes_pic_gen_eta_m21_m18[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >= -1.8 and mu.glb_gen_eta <= -1.5 ): h_ptRes_pic_gen_eta_m18_m15[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >= -1.5 and mu.glb_gen_eta <= -1.2 ): h_ptRes_pic_gen_eta_m15_m12[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >= -1.2 and mu.glb_gen_eta <= -0.9 ): h_ptRes_pic_gen_eta_m12_m09[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >= -0.9 and mu.glb_gen_eta <= -0.6 ): h_ptRes_pic_gen_eta_m09_m06[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >= -0.6 and mu.glb_gen_eta <= -0.3 ): h_ptRes_pic_gen_eta_m06_m03[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >= -0.3 and mu.glb_gen_eta <=  0.0 ): h_ptRes_pic_gen_eta_m03_m00[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  0.0 and mu.glb_gen_eta <=  0.3 ): h_ptRes_pic_gen_eta_p00_p03[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  0.3 and mu.glb_gen_eta <=  0.6 ): h_ptRes_pic_gen_eta_p03_p06[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  0.6 and mu.glb_gen_eta <=  0.9 ): h_ptRes_pic_gen_eta_p06_p09[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  0.9 and mu.glb_gen_eta <=  1.2 ): h_ptRes_pic_gen_eta_p09_p12[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  1.2 and mu.glb_gen_eta <=  1.5 ): h_ptRes_pic_gen_eta_p12_p15[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  1.5 and mu.glb_gen_eta <=  1.8 ): h_ptRes_pic_gen_eta_p15_p18[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  1.8 and mu.glb_gen_eta <=  2.1 ): h_ptRes_pic_gen_eta_p18_p21[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  2.1 and mu.glb_gen_eta <=  2.4 ): h_ptRes_pic_gen_eta_p21_p24[iSample].Fill(ptRes_pic_gen)
            # resolution vs phi
            if ( mu.glb_gen_phi >= -3.2 and mu.glb_gen_phi <= -2.8 ): h_ptRes_pic_gen_phi_m32_m28[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >= -2.8 and mu.glb_gen_phi <= -2.4 ): h_ptRes_pic_gen_phi_m28_m24[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >= -2.4 and mu.glb_gen_phi <= -2.0 ): h_ptRes_pic_gen_phi_m24_m20[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >= -2.0 and mu.glb_gen_phi <= -1.6 ): h_ptRes_pic_gen_phi_m20_m16[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >= -1.6 and mu.glb_gen_phi <= -1.2 ): h_ptRes_pic_gen_phi_m16_m12[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >= -1.2 and mu.glb_gen_phi <= -0.8 ): h_ptRes_pic_gen_phi_m12_m08[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >= -0.8 and mu.glb_gen_phi <= -0.4 ): h_ptRes_pic_gen_phi_m08_m04[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >= -0.4 and mu.glb_gen_phi <=  0.0 ): h_ptRes_pic_gen_phi_m04_m00[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >=  0.0 and mu.glb_gen_phi <=  0.4 ): h_ptRes_pic_gen_phi_p00_p04[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >=  0.4 and mu.glb_gen_phi <=  0.8 ): h_ptRes_pic_gen_phi_p04_p08[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >=  0.8 and mu.glb_gen_phi <=  1.2 ): h_ptRes_pic_gen_phi_p08_p12[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >=  1.2 and mu.glb_gen_phi <=  1.6 ): h_ptRes_pic_gen_phi_p12_p16[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >=  1.6 and mu.glb_gen_phi <=  2.0 ): h_ptRes_pic_gen_phi_p16_p20[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >=  2.0 and mu.glb_gen_phi <=  2.4 ): h_ptRes_pic_gen_phi_p20_p24[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >=  2.4 and mu.glb_gen_phi <=  2.8 ): h_ptRes_pic_gen_phi_p24_p28[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_phi >=  2.8 and mu.glb_gen_phi <=  3.2 ): h_ptRes_pic_gen_phi_p28_p32[iSample].Fill(ptRes_pic_gen)
            
            if ( mu.glb_gen_eta >=  -0.9 and mu.glb_gen_eta <=  0.9 ): 
              if ( mu.glb_gen_phi >= -3.2 and mu.glb_gen_phi <= -2.8 ): h_ptRes_pic_genB_phi_m32_m28[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.8 and mu.glb_gen_phi <= -2.4 ): h_ptRes_pic_genB_phi_m28_m24[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.4 and mu.glb_gen_phi <= -2.0 ): h_ptRes_pic_genB_phi_m24_m20[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.0 and mu.glb_gen_phi <= -1.6 ): h_ptRes_pic_genB_phi_m20_m16[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -1.6 and mu.glb_gen_phi <= -1.2 ): h_ptRes_pic_genB_phi_m16_m12[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -1.2 and mu.glb_gen_phi <= -0.8 ): h_ptRes_pic_genB_phi_m12_m08[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -0.8 and mu.glb_gen_phi <= -0.4 ): h_ptRes_pic_genB_phi_m08_m04[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -0.4 and mu.glb_gen_phi <=  0.0 ): h_ptRes_pic_genB_phi_m04_m00[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.0 and mu.glb_gen_phi <=  0.4 ): h_ptRes_pic_genB_phi_p00_p04[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.4 and mu.glb_gen_phi <=  0.8 ): h_ptRes_pic_genB_phi_p04_p08[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.8 and mu.glb_gen_phi <=  1.2 ): h_ptRes_pic_genB_phi_p08_p12[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  1.2 and mu.glb_gen_phi <=  1.6 ): h_ptRes_pic_genB_phi_p12_p16[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  1.6 and mu.glb_gen_phi <=  2.0 ): h_ptRes_pic_genB_phi_p16_p20[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.0 and mu.glb_gen_phi <=  2.4 ): h_ptRes_pic_genB_phi_p20_p24[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.4 and mu.glb_gen_phi <=  2.8 ): h_ptRes_pic_genB_phi_p24_p28[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.8 and mu.glb_gen_phi <=  3.2 ): h_ptRes_pic_genB_phi_p28_p32[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  0.9 and mu.glb_gen_eta <=  2.4 ): 
              if ( mu.glb_gen_phi >= -3.2 and mu.glb_gen_phi <= -2.8 ): h_ptRes_pic_genEOp_phi_m32_m28[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.8 and mu.glb_gen_phi <= -2.4 ): h_ptRes_pic_genEOp_phi_m28_m24[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.4 and mu.glb_gen_phi <= -2.0 ): h_ptRes_pic_genEOp_phi_m24_m20[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.0 and mu.glb_gen_phi <= -1.6 ): h_ptRes_pic_genEOp_phi_m20_m16[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -1.6 and mu.glb_gen_phi <= -1.2 ): h_ptRes_pic_genEOp_phi_m16_m12[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -1.2 and mu.glb_gen_phi <= -0.8 ): h_ptRes_pic_genEOp_phi_m12_m08[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -0.8 and mu.glb_gen_phi <= -0.4 ): h_ptRes_pic_genEOp_phi_m08_m04[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -0.4 and mu.glb_gen_phi <=  0.0 ): h_ptRes_pic_genEOp_phi_m04_m00[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.0 and mu.glb_gen_phi <=  0.4 ): h_ptRes_pic_genEOp_phi_p00_p04[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.4 and mu.glb_gen_phi <=  0.8 ): h_ptRes_pic_genEOp_phi_p04_p08[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.8 and mu.glb_gen_phi <=  1.2 ): h_ptRes_pic_genEOp_phi_p08_p12[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  1.2 and mu.glb_gen_phi <=  1.6 ): h_ptRes_pic_genEOp_phi_p12_p16[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  1.6 and mu.glb_gen_phi <=  2.0 ): h_ptRes_pic_genEOp_phi_p16_p20[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.0 and mu.glb_gen_phi <=  2.4 ): h_ptRes_pic_genEOp_phi_p20_p24[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.4 and mu.glb_gen_phi <=  2.8 ): h_ptRes_pic_genEOp_phi_p24_p28[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.8 and mu.glb_gen_phi <=  3.2 ): h_ptRes_pic_genEOp_phi_p28_p32[iSample].Fill(ptRes_pic_gen)
            if ( mu.glb_gen_eta >=  -2.4 and mu.glb_gen_eta <=  -0.9 ): 
              if ( mu.glb_gen_phi >= -3.2 and mu.glb_gen_phi <= -2.8 ): h_ptRes_pic_genEOm_phi_m32_m28[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.8 and mu.glb_gen_phi <= -2.4 ): h_ptRes_pic_genEOm_phi_m28_m24[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.4 and mu.glb_gen_phi <= -2.0 ): h_ptRes_pic_genEOm_phi_m24_m20[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -2.0 and mu.glb_gen_phi <= -1.6 ): h_ptRes_pic_genEOm_phi_m20_m16[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -1.6 and mu.glb_gen_phi <= -1.2 ): h_ptRes_pic_genEOm_phi_m16_m12[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -1.2 and mu.glb_gen_phi <= -0.8 ): h_ptRes_pic_genEOm_phi_m12_m08[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -0.8 and mu.glb_gen_phi <= -0.4 ): h_ptRes_pic_genEOm_phi_m08_m04[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >= -0.4 and mu.glb_gen_phi <=  0.0 ): h_ptRes_pic_genEOm_phi_m04_m00[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.0 and mu.glb_gen_phi <=  0.4 ): h_ptRes_pic_genEOm_phi_p00_p04[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.4 and mu.glb_gen_phi <=  0.8 ): h_ptRes_pic_genEOm_phi_p04_p08[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  0.8 and mu.glb_gen_phi <=  1.2 ): h_ptRes_pic_genEOm_phi_p08_p12[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  1.2 and mu.glb_gen_phi <=  1.6 ): h_ptRes_pic_genEOm_phi_p12_p16[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  1.6 and mu.glb_gen_phi <=  2.0 ): h_ptRes_pic_genEOm_phi_p16_p20[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.0 and mu.glb_gen_phi <=  2.4 ): h_ptRes_pic_genEOm_phi_p20_p24[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.4 and mu.glb_gen_phi <=  2.8 ): h_ptRes_pic_genEOm_phi_p24_p28[iSample].Fill(ptRes_pic_gen)
              if ( mu.glb_gen_phi >=  2.8 and mu.glb_gen_phi <=  3.2 ): h_ptRes_pic_genEOm_phi_p28_p32[iSample].Fill(ptRes_pic_gen)
        
        # pT resolution of GLB muons (tracker part only) w.r.t. GEN muons matched to the GLB muons
        if ( fillGenMuons and mu.glb and mu.glb_trk_pt > threshold_pT_GeV ):
          if ( mu.glb_gen_pt != 0.0 and mu.glb_trk_pt != 0.0 ):
            ptRes_gen_trk = mu.q/mu.glb_gen_pt - mu.q/mu.glb_trk_pt
            h_ptRes_gen_trk[iSample].Fill(ptRes_gen_trk)
            # resolution vs eta
            if ( mu.glb_trk_eta >= -2.4 and mu.glb_trk_eta <= -2.1 ): h_ptRes_gen_trk_eta_m24_m21[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >= -2.1 and mu.glb_trk_eta <= -1.8 ): h_ptRes_gen_trk_eta_m21_m18[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >= -1.8 and mu.glb_trk_eta <= -1.5 ): h_ptRes_gen_trk_eta_m18_m15[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >= -1.5 and mu.glb_trk_eta <= -1.2 ): h_ptRes_gen_trk_eta_m15_m12[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >= -1.2 and mu.glb_trk_eta <= -0.9 ): h_ptRes_gen_trk_eta_m12_m09[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >= -0.9 and mu.glb_trk_eta <= -0.6 ): h_ptRes_gen_trk_eta_m09_m06[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >= -0.6 and mu.glb_trk_eta <= -0.3 ): h_ptRes_gen_trk_eta_m06_m03[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >= -0.3 and mu.glb_trk_eta <=  0.0 ): h_ptRes_gen_trk_eta_m03_m00[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  0.0 and mu.glb_trk_eta <=  0.3 ): h_ptRes_gen_trk_eta_p00_p03[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  0.3 and mu.glb_trk_eta <=  0.6 ): h_ptRes_gen_trk_eta_p03_p06[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  0.6 and mu.glb_trk_eta <=  0.9 ): h_ptRes_gen_trk_eta_p06_p09[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  0.9 and mu.glb_trk_eta <=  1.2 ): h_ptRes_gen_trk_eta_p09_p12[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  1.2 and mu.glb_trk_eta <=  1.5 ): h_ptRes_gen_trk_eta_p12_p15[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  1.5 and mu.glb_trk_eta <=  1.8 ): h_ptRes_gen_trk_eta_p15_p18[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  1.8 and mu.glb_trk_eta <=  2.1 ): h_ptRes_gen_trk_eta_p18_p21[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  2.1 and mu.glb_trk_eta <=  2.4 ): h_ptRes_gen_trk_eta_p21_p24[iSample].Fill(ptRes_gen_trk)
            # resolution vs phi
            if ( mu.glb_trk_phi >= -3.2 and mu.glb_trk_phi <= -2.8 ): h_ptRes_gen_trk_phi_m32_m28[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >= -2.8 and mu.glb_trk_phi <= -2.4 ): h_ptRes_gen_trk_phi_m28_m24[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >= -2.4 and mu.glb_trk_phi <= -2.0 ): h_ptRes_gen_trk_phi_m24_m20[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >= -2.0 and mu.glb_trk_phi <= -1.6 ): h_ptRes_gen_trk_phi_m20_m16[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >= -1.6 and mu.glb_trk_phi <= -1.2 ): h_ptRes_gen_trk_phi_m16_m12[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >= -1.2 and mu.glb_trk_phi <= -0.8 ): h_ptRes_gen_trk_phi_m12_m08[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >= -0.8 and mu.glb_trk_phi <= -0.4 ): h_ptRes_gen_trk_phi_m08_m04[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >= -0.4 and mu.glb_trk_phi <=  0.0 ): h_ptRes_gen_trk_phi_m04_m00[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >=  0.0 and mu.glb_trk_phi <=  0.4 ): h_ptRes_gen_trk_phi_p00_p04[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >=  0.4 and mu.glb_trk_phi <=  0.8 ): h_ptRes_gen_trk_phi_p04_p08[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >=  0.8 and mu.glb_trk_phi <=  1.2 ): h_ptRes_gen_trk_phi_p08_p12[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >=  1.2 and mu.glb_trk_phi <=  1.6 ): h_ptRes_gen_trk_phi_p12_p16[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >=  1.6 and mu.glb_trk_phi <=  2.0 ): h_ptRes_gen_trk_phi_p16_p20[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >=  2.0 and mu.glb_trk_phi <=  2.4 ): h_ptRes_gen_trk_phi_p20_p24[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >=  2.4 and mu.glb_trk_phi <=  2.8 ): h_ptRes_gen_trk_phi_p24_p28[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_phi >=  2.8 and mu.glb_trk_phi <=  3.2 ): h_ptRes_gen_trk_phi_p28_p32[iSample].Fill(ptRes_gen_trk)
            
            if ( mu.glb_trk_eta >=  -0.9 and mu.glb_trk_eta <=  0.9 ): 
              if ( mu.glb_trk_phi >= -3.2 and mu.glb_trk_phi <= -2.8 ): h_ptRes_gen_trkB_phi_m32_m28[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.8 and mu.glb_trk_phi <= -2.4 ): h_ptRes_gen_trkB_phi_m28_m24[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.4 and mu.glb_trk_phi <= -2.0 ): h_ptRes_gen_trkB_phi_m24_m20[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.0 and mu.glb_trk_phi <= -1.6 ): h_ptRes_gen_trkB_phi_m20_m16[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -1.6 and mu.glb_trk_phi <= -1.2 ): h_ptRes_gen_trkB_phi_m16_m12[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -1.2 and mu.glb_trk_phi <= -0.8 ): h_ptRes_gen_trkB_phi_m12_m08[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -0.8 and mu.glb_trk_phi <= -0.4 ): h_ptRes_gen_trkB_phi_m08_m04[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -0.4 and mu.glb_trk_phi <=  0.0 ): h_ptRes_gen_trkB_phi_m04_m00[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.0 and mu.glb_trk_phi <=  0.4 ): h_ptRes_gen_trkB_phi_p00_p04[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.4 and mu.glb_trk_phi <=  0.8 ): h_ptRes_gen_trkB_phi_p04_p08[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.8 and mu.glb_trk_phi <=  1.2 ): h_ptRes_gen_trkB_phi_p08_p12[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  1.2 and mu.glb_trk_phi <=  1.6 ): h_ptRes_gen_trkB_phi_p12_p16[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  1.6 and mu.glb_trk_phi <=  2.0 ): h_ptRes_gen_trkB_phi_p16_p20[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.0 and mu.glb_trk_phi <=  2.4 ): h_ptRes_gen_trkB_phi_p20_p24[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.4 and mu.glb_trk_phi <=  2.8 ): h_ptRes_gen_trkB_phi_p24_p28[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.8 and mu.glb_trk_phi <=  3.2 ): h_ptRes_gen_trkB_phi_p28_p32[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  0.9 and mu.glb_trk_eta <=  2.4 ): 
              if ( mu.glb_trk_phi >= -3.2 and mu.glb_trk_phi <= -2.8 ): h_ptRes_gen_trkEOp_phi_m32_m28[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.8 and mu.glb_trk_phi <= -2.4 ): h_ptRes_gen_trkEOp_phi_m28_m24[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.4 and mu.glb_trk_phi <= -2.0 ): h_ptRes_gen_trkEOp_phi_m24_m20[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.0 and mu.glb_trk_phi <= -1.6 ): h_ptRes_gen_trkEOp_phi_m20_m16[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -1.6 and mu.glb_trk_phi <= -1.2 ): h_ptRes_gen_trkEOp_phi_m16_m12[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -1.2 and mu.glb_trk_phi <= -0.8 ): h_ptRes_gen_trkEOp_phi_m12_m08[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -0.8 and mu.glb_trk_phi <= -0.4 ): h_ptRes_gen_trkEOp_phi_m08_m04[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -0.4 and mu.glb_trk_phi <=  0.0 ): h_ptRes_gen_trkEOp_phi_m04_m00[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.0 and mu.glb_trk_phi <=  0.4 ): h_ptRes_gen_trkEOp_phi_p00_p04[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.4 and mu.glb_trk_phi <=  0.8 ): h_ptRes_gen_trkEOp_phi_p04_p08[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.8 and mu.glb_trk_phi <=  1.2 ): h_ptRes_gen_trkEOp_phi_p08_p12[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  1.2 and mu.glb_trk_phi <=  1.6 ): h_ptRes_gen_trkEOp_phi_p12_p16[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  1.6 and mu.glb_trk_phi <=  2.0 ): h_ptRes_gen_trkEOp_phi_p16_p20[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.0 and mu.glb_trk_phi <=  2.4 ): h_ptRes_gen_trkEOp_phi_p20_p24[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.4 and mu.glb_trk_phi <=  2.8 ): h_ptRes_gen_trkEOp_phi_p24_p28[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.8 and mu.glb_trk_phi <=  3.2 ): h_ptRes_gen_trkEOp_phi_p28_p32[iSample].Fill(ptRes_gen_trk)
            if ( mu.glb_trk_eta >=  -2.4 and mu.glb_trk_eta <=  -0.9 ): 
              if ( mu.glb_trk_phi >= -3.2 and mu.glb_trk_phi <= -2.8 ): h_ptRes_gen_trkEOm_phi_m32_m28[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.8 and mu.glb_trk_phi <= -2.4 ): h_ptRes_gen_trkEOm_phi_m28_m24[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.4 and mu.glb_trk_phi <= -2.0 ): h_ptRes_gen_trkEOm_phi_m24_m20[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -2.0 and mu.glb_trk_phi <= -1.6 ): h_ptRes_gen_trkEOm_phi_m20_m16[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -1.6 and mu.glb_trk_phi <= -1.2 ): h_ptRes_gen_trkEOm_phi_m16_m12[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -1.2 and mu.glb_trk_phi <= -0.8 ): h_ptRes_gen_trkEOm_phi_m12_m08[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -0.8 and mu.glb_trk_phi <= -0.4 ): h_ptRes_gen_trkEOm_phi_m08_m04[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >= -0.4 and mu.glb_trk_phi <=  0.0 ): h_ptRes_gen_trkEOm_phi_m04_m00[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.0 and mu.glb_trk_phi <=  0.4 ): h_ptRes_gen_trkEOm_phi_p00_p04[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.4 and mu.glb_trk_phi <=  0.8 ): h_ptRes_gen_trkEOm_phi_p04_p08[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  0.8 and mu.glb_trk_phi <=  1.2 ): h_ptRes_gen_trkEOm_phi_p08_p12[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  1.2 and mu.glb_trk_phi <=  1.6 ): h_ptRes_gen_trkEOm_phi_p12_p16[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  1.6 and mu.glb_trk_phi <=  2.0 ): h_ptRes_gen_trkEOm_phi_p16_p20[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.0 and mu.glb_trk_phi <=  2.4 ): h_ptRes_gen_trkEOm_phi_p20_p24[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.4 and mu.glb_trk_phi <=  2.8 ): h_ptRes_gen_trkEOm_phi_p24_p28[iSample].Fill(ptRes_gen_trk)
              if ( mu.glb_trk_phi >=  2.8 and mu.glb_trk_phi <=  3.2 ): h_ptRes_gen_trkEOm_phi_p28_p32[iSample].Fill(ptRes_gen_trk)
        
    if ( fillRecoDimuons ):
      counterRecoDimuons = 0 # reset counter for every file
      treeName = "muAlAnalyzer/recoDimuons"
      print >> sys.stderr, "      Read tree", treeName
      recoDimuons = tfile.Get(treeName)
      print >> sys.stderr, "         Total number of entries in the tree:", recoDimuons.GetEntriesFast()
      
      for dm in recoDimuons:
        if maxEntries > 0 and counterRecoDimuons >= maxEntries:
          break
        if ( not counterRecoDimuons%10000 ):
          print >> sys.stderr, counterRecoDimuons
        counterRecoDimuons = counterRecoDimuons + 1
        if ( dm.sta and dm.glb and dm.pos_glb_trk_pt > threshold_pT_GeV and dm.neg_glb_trk_pt > threshold_pT_GeV):
          h_m_sta[iSample].Fill(dm.sta_m)
          
          # resolution vs eta of the sta muon
          RandmonNumber=randint(0,1) # generate or 0 or 1
          hybridMu1 = TLorentzVector(); hybridMu2 = TLorentzVector();
          if(RandmonNumber>0.5):
            hybridMu1.SetPtEtaPhiM(dm.pos_sta_pt,dm.pos_sta_eta,dm.pos_sta_phi,0)
            hybridMu2.SetPtEtaPhiM(dm.neg_glb_pt,dm.neg_glb_eta,dm.neg_glb_phi,0)
            etaSta=dm.pos_sta_eta
            phiSta=dm.pos_sta_phi
          else:
            hybridMu1.SetPtEtaPhiM(dm.pos_glb_pt,dm.pos_glb_eta,dm.pos_glb_phi,0)
            hybridMu2.SetPtEtaPhiM(dm.neg_sta_pt,dm.neg_sta_eta,dm.neg_sta_phi,0)
            etaSta=dm.neg_sta_eta
            phiSta=dm.neg_sta_phi
          hybridZ = TLorentzVector(); hybridZ=hybridMu1+hybridMu2
          if( fabs(dm.glb_m-91.)<5. ):     
            # Hybrid Z vs Eta
            if ( etaSta >= -2.4 and etaSta <= -2.1 ): h_m_HybSta_etaSta_m24_m21[iSample].Fill(hybridZ.M())
            if ( etaSta >= -2.1 and etaSta <= -1.8 ): h_m_HybSta_etaSta_m21_m18[iSample].Fill(hybridZ.M())
            if ( etaSta >= -1.8 and etaSta <= -1.5 ): h_m_HybSta_etaSta_m18_m15[iSample].Fill(hybridZ.M())
            if ( etaSta >= -1.5 and etaSta <= -1.2 ): h_m_HybSta_etaSta_m15_m12[iSample].Fill(hybridZ.M())
            if ( etaSta >= -1.2 and etaSta <= -0.9 ): h_m_HybSta_etaSta_m12_m09[iSample].Fill(hybridZ.M())
            if ( etaSta >= -0.9 and etaSta <= -0.6 ): h_m_HybSta_etaSta_m09_m06[iSample].Fill(hybridZ.M())
            if ( etaSta >= -0.6 and etaSta <= -0.3 ): h_m_HybSta_etaSta_m06_m03[iSample].Fill(hybridZ.M())
            if ( etaSta >= -0.3 and etaSta <=  0.0 ): h_m_HybSta_etaSta_m03_m00[iSample].Fill(hybridZ.M())
            if ( etaSta >=  0.0 and etaSta <=  0.3 ): h_m_HybSta_etaSta_p00_p03[iSample].Fill(hybridZ.M())
            if ( etaSta >=  0.3 and etaSta <=  0.6 ): h_m_HybSta_etaSta_p03_p06[iSample].Fill(hybridZ.M())
            if ( etaSta >=  0.6 and etaSta <=  0.9 ): h_m_HybSta_etaSta_p06_p09[iSample].Fill(hybridZ.M())
            if ( etaSta >=  0.9 and etaSta <=  1.2 ): h_m_HybSta_etaSta_p09_p12[iSample].Fill(hybridZ.M())
            if ( etaSta >=  1.2 and etaSta <=  1.5 ): h_m_HybSta_etaSta_p12_p15[iSample].Fill(hybridZ.M())
            if ( etaSta >=  1.5 and etaSta <=  1.8 ): h_m_HybSta_etaSta_p15_p18[iSample].Fill(hybridZ.M())
            if ( etaSta >=  1.8 and etaSta <=  2.1 ): h_m_HybSta_etaSta_p18_p21[iSample].Fill(hybridZ.M())
            if ( etaSta >=  2.1 and etaSta <=  2.4 ): h_m_HybSta_etaSta_p21_p24[iSample].Fill(hybridZ.M())
            # Hybrid Z vs Phi
            if ( phiSta >= -3.2 and phiSta <= -2.8 ): h_m_HybSta_phiSta_m32_m28[iSample].Fill(hybridZ.M())
            if ( phiSta >= -2.8 and phiSta <= -2.4 ): h_m_HybSta_phiSta_m28_m24[iSample].Fill(hybridZ.M())
            if ( phiSta >= -2.4 and phiSta <= -2.0 ): h_m_HybSta_phiSta_m24_m20[iSample].Fill(hybridZ.M())
            if ( phiSta >= -2.0 and phiSta <= -1.6 ): h_m_HybSta_phiSta_m20_m16[iSample].Fill(hybridZ.M())
            if ( phiSta >= -1.6 and phiSta <= -1.2 ): h_m_HybSta_phiSta_m16_m12[iSample].Fill(hybridZ.M())
            if ( phiSta >= -1.2 and phiSta <= -0.8 ): h_m_HybSta_phiSta_m12_m08[iSample].Fill(hybridZ.M())
            if ( phiSta >= -0.8 and phiSta <= -0.4 ): h_m_HybSta_phiSta_m08_m04[iSample].Fill(hybridZ.M())
            if ( phiSta >= -0.4 and phiSta <=  0.0 ): h_m_HybSta_phiSta_m04_m00[iSample].Fill(hybridZ.M())
            if ( phiSta >=  0.0 and phiSta <=  0.4 ): h_m_HybSta_phiSta_p00_p04[iSample].Fill(hybridZ.M())
            if ( phiSta >=  0.4 and phiSta <=  0.8 ): h_m_HybSta_phiSta_p04_p08[iSample].Fill(hybridZ.M())
            if ( phiSta >=  0.8 and phiSta <=  1.2 ): h_m_HybSta_phiSta_p08_p12[iSample].Fill(hybridZ.M())
            if ( phiSta >=  1.2 and phiSta <=  1.6 ): h_m_HybSta_phiSta_p12_p16[iSample].Fill(hybridZ.M())
            if ( phiSta >=  1.6 and phiSta <=  2.0 ): h_m_HybSta_phiSta_p16_p20[iSample].Fill(hybridZ.M())
            if ( phiSta >=  2.0 and phiSta <=  2.4 ): h_m_HybSta_phiSta_p20_p24[iSample].Fill(hybridZ.M())
            if ( phiSta >=  2.4 and phiSta <=  2.8 ): h_m_HybSta_phiSta_p24_p28[iSample].Fill(hybridZ.M())
            if ( phiSta >=  2.8 and phiSta <=  3.2 ): h_m_HybSta_phiSta_p28_p32[iSample].Fill(hybridZ.M())


          # resolution vs eta
          if ( dm.pos_sta_eta >= -2.4 and dm.pos_sta_eta <= -2.1 ): h_m_sta_etaMuP_m24_m21[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >= -2.1 and dm.pos_sta_eta <= -1.8 ): h_m_sta_etaMuP_m21_m18[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >= -1.8 and dm.pos_sta_eta <= -1.5 ): h_m_sta_etaMuP_m18_m15[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >= -1.5 and dm.pos_sta_eta <= -1.2 ): h_m_sta_etaMuP_m15_m12[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >= -1.2 and dm.pos_sta_eta <= -0.9 ): h_m_sta_etaMuP_m12_m09[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >= -0.9 and dm.pos_sta_eta <= -0.6 ): h_m_sta_etaMuP_m09_m06[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >= -0.6 and dm.pos_sta_eta <= -0.3 ): h_m_sta_etaMuP_m06_m03[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >= -0.3 and dm.pos_sta_eta <=  0.0 ): h_m_sta_etaMuP_m03_m00[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  0.0 and dm.pos_sta_eta <=  0.3 ): h_m_sta_etaMuP_p00_p03[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  0.3 and dm.pos_sta_eta <=  0.6 ): h_m_sta_etaMuP_p03_p06[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  0.6 and dm.pos_sta_eta <=  0.9 ): h_m_sta_etaMuP_p06_p09[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  0.9 and dm.pos_sta_eta <=  1.2 ): h_m_sta_etaMuP_p09_p12[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  1.2 and dm.pos_sta_eta <=  1.5 ): h_m_sta_etaMuP_p12_p15[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  1.5 and dm.pos_sta_eta <=  1.8 ): h_m_sta_etaMuP_p15_p18[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  1.8 and dm.pos_sta_eta <=  2.1 ): h_m_sta_etaMuP_p18_p21[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  2.1 and dm.pos_sta_eta <=  2.4 ): h_m_sta_etaMuP_p21_p24[iSample].Fill(dm.sta_m)
          # resolution vs phi
          if ( dm.pos_sta_phi >= -3.2 and dm.pos_sta_phi <= -2.8 ): h_m_sta_phiMuP_m32_m28[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >= -2.8 and dm.pos_sta_phi <= -2.4 ): h_m_sta_phiMuP_m28_m24[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >= -2.4 and dm.pos_sta_phi <= -2.0 ): h_m_sta_phiMuP_m24_m20[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >= -2.0 and dm.pos_sta_phi <= -1.6 ): h_m_sta_phiMuP_m20_m16[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >= -1.6 and dm.pos_sta_phi <= -1.2 ): h_m_sta_phiMuP_m16_m12[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >= -1.2 and dm.pos_sta_phi <= -0.8 ): h_m_sta_phiMuP_m12_m08[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >= -0.8 and dm.pos_sta_phi <= -0.4 ): h_m_sta_phiMuP_m08_m04[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >= -0.4 and dm.pos_sta_phi <=  0.0 ): h_m_sta_phiMuP_m04_m00[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >=  0.0 and dm.pos_sta_phi <=  0.4 ): h_m_sta_phiMuP_p00_p04[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >=  0.4 and dm.pos_sta_phi <=  0.8 ): h_m_sta_phiMuP_p04_p08[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >=  0.8 and dm.pos_sta_phi <=  1.2 ): h_m_sta_phiMuP_p08_p12[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >=  1.2 and dm.pos_sta_phi <=  1.6 ): h_m_sta_phiMuP_p12_p16[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >=  1.6 and dm.pos_sta_phi <=  2.0 ): h_m_sta_phiMuP_p16_p20[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >=  2.0 and dm.pos_sta_phi <=  2.4 ): h_m_sta_phiMuP_p20_p24[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >=  2.4 and dm.pos_sta_phi <=  2.8 ): h_m_sta_phiMuP_p24_p28[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_phi >=  2.8 and dm.pos_sta_phi <=  3.2 ): h_m_sta_phiMuP_p28_p32[iSample].Fill(dm.sta_m)
          
          if ( dm.pos_sta_eta >=  -0.9 and dm.pos_sta_eta <=  0.9 ): 
            if ( dm.pos_sta_phi >= -3.2 and dm.pos_sta_phi <= -2.8 ): h_m_staB_phiMuP_m32_m28[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.8 and dm.pos_sta_phi <= -2.4 ): h_m_staB_phiMuP_m28_m24[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.4 and dm.pos_sta_phi <= -2.0 ): h_m_staB_phiMuP_m24_m20[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.0 and dm.pos_sta_phi <= -1.6 ): h_m_staB_phiMuP_m20_m16[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -1.6 and dm.pos_sta_phi <= -1.2 ): h_m_staB_phiMuP_m16_m12[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -1.2 and dm.pos_sta_phi <= -0.8 ): h_m_staB_phiMuP_m12_m08[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -0.8 and dm.pos_sta_phi <= -0.4 ): h_m_staB_phiMuP_m08_m04[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -0.4 and dm.pos_sta_phi <=  0.0 ): h_m_staB_phiMuP_m04_m00[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.0 and dm.pos_sta_phi <=  0.4 ): h_m_staB_phiMuP_p00_p04[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.4 and dm.pos_sta_phi <=  0.8 ): h_m_staB_phiMuP_p04_p08[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.8 and dm.pos_sta_phi <=  1.2 ): h_m_staB_phiMuP_p08_p12[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  1.2 and dm.pos_sta_phi <=  1.6 ): h_m_staB_phiMuP_p12_p16[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  1.6 and dm.pos_sta_phi <=  2.0 ): h_m_staB_phiMuP_p16_p20[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.0 and dm.pos_sta_phi <=  2.4 ): h_m_staB_phiMuP_p20_p24[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.4 and dm.pos_sta_phi <=  2.8 ): h_m_staB_phiMuP_p24_p28[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.8 and dm.pos_sta_phi <=  3.2 ): h_m_staB_phiMuP_p28_p32[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  0.9 and dm.pos_sta_eta <=  2.4 ): 
            if ( dm.pos_sta_phi >= -3.2 and dm.pos_sta_phi <= -2.8 ): h_m_staEOp_phiMuP_m32_m28[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.8 and dm.pos_sta_phi <= -2.4 ): h_m_staEOp_phiMuP_m28_m24[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.4 and dm.pos_sta_phi <= -2.0 ): h_m_staEOp_phiMuP_m24_m20[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.0 and dm.pos_sta_phi <= -1.6 ): h_m_staEOp_phiMuP_m20_m16[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -1.6 and dm.pos_sta_phi <= -1.2 ): h_m_staEOp_phiMuP_m16_m12[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -1.2 and dm.pos_sta_phi <= -0.8 ): h_m_staEOp_phiMuP_m12_m08[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -0.8 and dm.pos_sta_phi <= -0.4 ): h_m_staEOp_phiMuP_m08_m04[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -0.4 and dm.pos_sta_phi <=  0.0 ): h_m_staEOp_phiMuP_m04_m00[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.0 and dm.pos_sta_phi <=  0.4 ): h_m_staEOp_phiMuP_p00_p04[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.4 and dm.pos_sta_phi <=  0.8 ): h_m_staEOp_phiMuP_p04_p08[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.8 and dm.pos_sta_phi <=  1.2 ): h_m_staEOp_phiMuP_p08_p12[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  1.2 and dm.pos_sta_phi <=  1.6 ): h_m_staEOp_phiMuP_p12_p16[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  1.6 and dm.pos_sta_phi <=  2.0 ): h_m_staEOp_phiMuP_p16_p20[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.0 and dm.pos_sta_phi <=  2.4 ): h_m_staEOp_phiMuP_p20_p24[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.4 and dm.pos_sta_phi <=  2.8 ): h_m_staEOp_phiMuP_p24_p28[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.8 and dm.pos_sta_phi <=  3.2 ): h_m_staEOp_phiMuP_p28_p32[iSample].Fill(dm.sta_m)
          if ( dm.pos_sta_eta >=  -2.4 and dm.pos_sta_eta <=  -0.9 ): 
            if ( dm.pos_sta_phi >= -3.2 and dm.pos_sta_phi <= -2.8 ): h_m_staEOm_phiMuP_m32_m28[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.8 and dm.pos_sta_phi <= -2.4 ): h_m_staEOm_phiMuP_m28_m24[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.4 and dm.pos_sta_phi <= -2.0 ): h_m_staEOm_phiMuP_m24_m20[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -2.0 and dm.pos_sta_phi <= -1.6 ): h_m_staEOm_phiMuP_m20_m16[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -1.6 and dm.pos_sta_phi <= -1.2 ): h_m_staEOm_phiMuP_m16_m12[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -1.2 and dm.pos_sta_phi <= -0.8 ): h_m_staEOm_phiMuP_m12_m08[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -0.8 and dm.pos_sta_phi <= -0.4 ): h_m_staEOm_phiMuP_m08_m04[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >= -0.4 and dm.pos_sta_phi <=  0.0 ): h_m_staEOm_phiMuP_m04_m00[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.0 and dm.pos_sta_phi <=  0.4 ): h_m_staEOm_phiMuP_p00_p04[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.4 and dm.pos_sta_phi <=  0.8 ): h_m_staEOm_phiMuP_p04_p08[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  0.8 and dm.pos_sta_phi <=  1.2 ): h_m_staEOm_phiMuP_p08_p12[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  1.2 and dm.pos_sta_phi <=  1.6 ): h_m_staEOm_phiMuP_p12_p16[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  1.6 and dm.pos_sta_phi <=  2.0 ): h_m_staEOm_phiMuP_p16_p20[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.0 and dm.pos_sta_phi <=  2.4 ): h_m_staEOm_phiMuP_p20_p24[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.4 and dm.pos_sta_phi <=  2.8 ): h_m_staEOm_phiMuP_p24_p28[iSample].Fill(dm.sta_m)
            if ( dm.pos_sta_phi >=  2.8 and dm.pos_sta_phi <=  3.2 ): h_m_staEOm_phiMuP_p28_p32[iSample].Fill(dm.sta_m)
    
      print >> sys.stderr, "         Processed number of entries:", counterRecoMuons
      


