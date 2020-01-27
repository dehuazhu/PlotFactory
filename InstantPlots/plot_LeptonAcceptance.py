import ROOT
from pdb import set_trace
import numpy as np
import plotfactory
import glob

# ROOT.ROOT.EnableImplicitMT()

def makeChain(samplesPath, singleFile = False):
    plotfactory.setpfstyle()
    chain = ROOT.TChain('tree')

    all_files = glob.glob(samplesPath + '*/HNLTreeProducer*/tree.root')
    nfiles = len(all_files)

    if singleFile == False:
        for file in all_files:
            chain.Add(file)

    elif singleFile == True:
        chain.Add('/Users/dehuazhu/SynologyDrive/PhD/5_Projects/analysis/200114_AcceptancePlots/signals_2018/HN3L_M_2_V_0p0307896086367_mu_Dirac_cc_massiveAndCKM_LO/HNLTreeProducer_mmm/tree.root')

    return chain, nfiles

def makeEffPlot(channel = 'mu', color = ROOT.kBlack):
    # xbins = np.logspace(-2, 1.6, 10) # 50 evenly spaced points from 10^-3 to 10^3 cm 
    # xbins = np.logspace(-2, 3, 10) # 50 evenly spaced points from 10^-3 to 10^3 cm 
    # xbins = np.arange(0, 100, 5) # 50 evenly spaced points from 10^-3 to 10^3 cm 
    xbins = np.array([0.0,2.9,6.8,10.9,16.0,110.0,180.,280.,380.,720.,1000.])
    
    if channel == 'mu' : pdgid = 13
    if channel == 'ele': pdgid = 11

    sel_denominator_l1 = '(l1_gen_pdgid == %d || l1_gen_pdgid == -%d) && l1_gen_eta < 2.4 && l1_gen_eta > -2.4 && l1_gen_pt > 7'%(pdgid,pdgid)
    sel_enumerator_l1  = sel_denominator_l1 + ' && l1_good_match < 0.1 && l1_gen_match_pt > 0 && (l1_gen_match_pdgid == %d || l1_gen_match_pdgid == -%d)'%(pdgid,pdgid) #it's delta R
    sel_denominator_l2 = '(l2_gen_pdgid == %d || l2_gen_pdgid == -%d) && l2_gen_eta < 2.4 && l2_gen_eta > -2.4 && l2_gen_pt > 7'%(pdgid,pdgid)
    sel_enumerator_l2  = sel_denominator_l2 + ' && l2_good_match < 0.1 && l2_gen_match_pt > 0 && (l2_gen_match_pdgid == %d || l2_gen_match_pdgid == -%d)'%(pdgid,pdgid) #it's delta R

    h_denominator_l1 = dataframe.Filter(sel_denominator_l1).Histo1D(('','',len(xbins)-1,xbins),'hnl_2d_gen_disp')
    h_denominator_l1 = h_denominator_l1.Clone() 
    h_enumerator_l1  = dataframe.Filter(sel_enumerator_l1 ).Histo1D(('','',len(xbins)-1,xbins),'hnl_2d_gen_disp')
    h_enumerator_l1  = h_enumerator_l1.Clone() 

    h_denominator_l2 = dataframe.Filter(sel_denominator_l2).Histo1D(('','',len(xbins)-1,xbins),'hnl_2d_gen_disp')
    h_denominator_l2 = h_denominator_l2.Clone() 
    h_enumerator_l2  = dataframe.Filter(sel_enumerator_l2 ).Histo1D(('','',len(xbins)-1,xbins),'hnl_2d_gen_disp')
    h_enumerator_l2  = h_enumerator_l2.Clone() 

    h_denominator_mu = h_denominator_l1 + h_denominator_l2
    h_enumerator_mu  = h_enumerator_l1  + h_enumerator_l2

    # h_enumerator_mu_l1.Divide(h_denominator_mu_l1)
    effPlot = ROOT.TEfficiency(h_enumerator_mu,h_denominator_mu)
    effPlot.SetTitle(';transverse production radius (cm); reconstruction efficiency')
    effPlot.SetMarkerColor(color)
    effPlot.SetLineColor(color)

    return effPlot

if __name__ == "__main__":
    samplesPath = '/Users/dehuazhu/SynologyDrive/PhD/5_Projects/analysis/200114_AcceptancePlots/20200117_signals_2018_m/'
    singleFile = False
    chain, nfiles = makeChain(samplesPath, singleFile = singleFile)
    dataframe = ROOT.ROOT.RDataFrame(chain)
    print('created dataframe with %d entries'%(dataframe.Count().GetValue()))
    
    eff_mu  = makeEffPlot(channel = 'mu', color = ROOT.kBlue + 2)
    eff_ele = makeEffPlot(channel = 'ele', color = ROOT.kRed + 2)

    can = ROOT.TCanvas()
    eff_mu .Draw()
    eff_ele.Draw('same')

    leg = ROOT.TLegend(.2,.25,.5,.38)
    leg.AddEntry(eff_mu, 'muon','EP')
    leg.AddEntry(eff_ele, 'electron', 'EP')
    leg.Draw('apez same')

    plotfactory.showlogopreliminary()

    can.SetLogx()
    can.Update()
    can.SaveAs('Acceptanceplots/LeptonAcceptance.pdf')
    can.SaveAs('Acceptanceplots/LeptonAcceptance.png')
    can.SaveAs('Acceptanceplots/LeptonAcceptance.root')
    can.SaveAs('Acceptanceplots/LeptonAcceptance.tex')
    set_trace()



