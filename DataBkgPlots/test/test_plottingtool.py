import ROOT
# import plotfactory as pf
import numpy as np
import sys
from pdb import set_trace

# pf.setpfstyle()

t = ROOT.TChain('tree')
# t.Add('/mnt/StorageElement1/4_production/2018/production_20190924_Bkg_mmm/DYJetsToLL_M50_ext/HNLTreeProducer/tree.root')
t.Add('/mnt/StorageElement1/4_production/2018/production_20191027_Signal_mmm/HN3L_M_5_V_0p00145602197786_mu_massiveAndCKM_LO/HNLTreeProducer/tree.root')

# chain = ROOT.TChain('tree')
# chain.Add('/mnt/StorageElement1/4_production/2018/production_20190924_Bkg_mmm/WW/HNLTreeProducer/tree.root')
# chain.Add('/mnt/StorageElement1/4_production/2018/production_20190924_Bkg_mmm/WZ/HNLTreeProducer/tree.root')
# chain.Add('/mnt/StorageElement1/4_production/2018/production_20190924_Bkg_mmm/ZZ/HNLTreeProducer/tree.root')

# binsx = np.arange(0.,200.,5.)
# binsx = np.arange(0.,3.,1.)
binsx = np.arange(0.,6.,1.)
# set_trace()

can = ROOT.TCanvas('can','can')

hist = ROOT.TH1F('h','h',len(binsx)-1,binsx)

# L_data = 41000
# L_data = 14000.
L_data = 59740.0 # 2018, all eras
# xsec = 2075.14*3 
xsec = 0.008434 # for 2018 signal
# xsec = 1.
# N_events = 158048935. #v1.0
# SumWeights = 5939397. #v2.0, using the SumNormWeights from SkimAnalyzercount/SkimReport.txt
# SumWeights = 123584524. #v2.0, higher stats
# SumWeights = 117868913. #v2.0, 20190402
SumWeights = 249792. # 2018 signal
L_MC   = SumWeights /xsec

L_ratio = L_data/L_MC # L_ratio = 4.106083204928521


selection = "((l0_pt > 25  & abs(l0_eta) < 2.4  & abs(l0_dxy) < 0.05  & abs(l0_dz) < 0.2  & l0_reliso_rho_03 < 0.2  & l1_pt > 5  & abs(l1_eta) < 2.4  & abs(l1_dxy) > 0.01  & l2_pt > 5  & abs(l2_eta) < 2.4  & abs(l2_dxy) > 0.01  & hnl_q_12 == 0  & min(abs(hnl_dphi_01), abs(hnl_dphi_02))>1. & hnl_dr_12 < 1. & (nbj == 0) & (hnl_w_vis_m > 50. && hnl_w_vis_m < 80.)  & sv_cos > 0.&abs(hnl_m_12-3.0969) > 0.08&abs(hnl_m_12-3.6861) > 0.08&abs(hnl_m_12-0.7827) > 0.08&abs(hnl_m_12-1.0190) > 0.08&!(hnl_q_01==0 & abs(hnl_m_01-91.1876) < 10)&!(hnl_q_01==0 & abs(hnl_m_01- 9.4603) < 0.08)&!(hnl_q_01==0 & abs(hnl_m_01-10.0233) < 0.08)&!(hnl_q_01==0 & abs(hnl_m_01-10.3552) < 0.08)&!(hnl_q_01==0 & abs(hnl_m_01-3.0969) < 0.08)&!(hnl_q_01==0 & abs(hnl_m_01-3.6861) < 0.08)&!(hnl_q_01==0 & abs(hnl_m_01-0.7827) < 0.08)&!(hnl_q_01==0 & abs(hnl_m_01-1.0190) < 0.08)&!(hnl_q_02==0 & abs(hnl_m_02-91.1876) < 10)&!(hnl_q_02==0 & abs(hnl_m_02- 9.4603) < 0.08)&!(hnl_q_02==0 & abs(hnl_m_02-10.0233) < 0.08)&!(hnl_q_02==0 & abs(hnl_m_02-10.3552) < 0.08)&!(hnl_q_02==0 & abs(hnl_m_02-3.0969) < 0.08)&!(hnl_q_02==0 & abs(hnl_m_02-3.6861) < 0.08)&!(hnl_q_02==0 & abs(hnl_m_02-0.7827) < 0.08)&!(hnl_q_02==0 & abs(hnl_m_02-1.0190) < 0.08)&l0_id_m == 1&l1_Medium == 1 &l2_Medium == 1 ) && (l1_reliso_rho_03 < 0.2 && l2_reliso_rho_03 < 0.2 )) && (hnl_2d_disp < 0.5)"

weight = 'weight * lhe_weight'
# weight = 'weight '
lumi_correction = L_ratio
set_trace()


# final_selection = '(%s)'%(selection) 
# final_selection = '(%s)*(%s)'%(selection,weight) 
final_selection = '(%s)*(%s)*(%f)'%(selection,weight,lumi_correction) 

# weight2 = '(l0_pt>25 & abs(l0_eta)<2.4 & (l0_q != l1_q) & l1_pt > 15 & abs(l1_eta) < 2.4 & abs(l0_dxy) < 0.05 & abs(l0_dz) < 0.2 & abs(l1_dxy) < 0.05 & abs(l1_dz) < 0.2 & nbj == 0 & & l0_id_t & l1_id_t& l2_id_m & l0_reliso05_03 < 0.15& l1_reliso05_03 < 0.15& l2_reliso05_03 < 0.15& abs(l2_gen_match_pdgid) != 22 ) * weight * lhe_weight'

# t.Draw("hnl_m_01 >> h",'(%s)*(%s)'%(selection,weight))
# t.Draw("hnl_m_01 >> h",weight2)
# t.Draw("hnl_m_01 >> hist",final_selection)
# t.Draw("hnl_m_12 >> hist",final_selection)
t.Draw("hnl_m_12 >> histo(5,0,5)",final_selection)
# t.Draw("hnl_m_01 >> h",selection + '* weight * lhe_weight * %d'%(lumi_correction))
can.Update()

# cn = ROOT.TCanvas('cn','cn')
# t.Draw("1 >> HISTO(1, 0, 2)", final_selection)
# integral = ROOT.gDirectory.Get('HISTO').Integral()
# n_events = ROOT.gDirectory.Get('HISTO').GetEntries()
# print 'The n_events of the histogram is %d'%(n_events)
# print 'The integral of the histogram is %d'%(integral)
# cn.Update()

set_trace()

