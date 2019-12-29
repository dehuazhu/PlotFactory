import ROOT
import plotfactory
from glob import glob
from pdb import set_trace
import numpy as np
import imp
Selections = imp.load_source('Region', '/Users/dehuazhu/gitprojects/PlotFactory/DataBkgPlots/modules/Selections.py')
ROOT.ROOT.EnableImplicitMT()

def makechain():
    chain = ROOT.TChain('tree')
    # all_files = glob('/mnt/StorageElement1/7_NN/2018/mmm_nonprompt_v8_Endgame/friendtree_fr_nonprompt*')
    # all_files = glob('/Users/dehuazhu/data/mmm_nonprompt_v8_Endgame/friendtree_fr_nonprompt*')
    all_files = glob('/Users/dehuazhu/data/mmm_nonprompt_v8_Endgame/Single_mu_2018*/HNLTreeProducer/tree.root')
    for sample in all_files:
        chain.Add(sample)
    # print('Created a TChain object with %d entries.'%chain.GetEntries())
    return chain

def makeFakeRatePlot(varName):
    tt = makechain()
    dataframe = ROOT.RDataFrame(tt)
    plotfactory.setpfstyle()
    can = ROOT.TCanvas('c1','c1')

    print('running variable %s'%varName)

    if varName == 'l1_pt':      binsx = np.array([0.,5.,10.,15.,20.,30.,50.,70.]) # for pt
    if varName == 'abs_l1_eta':     binsx = np.arange(0.    ,2.5    ,0.4)
    if varName == 'abs_l1_dxy':     binsx = np.logspace(-1.9,-1.4,5)
    if varName == 'abs_l1_dz':      binsx = np.logspace(-1.8,-0.5,10)
    if varName == 'hnl_2d_disp':    binsx = np.logspace(-0.7   ,0.4    ,5)
    if varName == 'hnl_dr_12':      binsx = np.logspace(-1.3     , -0.4    ,9) 
    if varName == 'hnl_m_12':       binsx = np.arange(1.,   4.,    0.5)
    if varName == 'sv_prob':        binsx = np.arange(0.,   1.0,    0.1)
    if varName == 'hnl_w_vis_m':    binsx = np.arange(0.,   200.0,    30)
    # if varName == 'sv_prob':        binsx = np.logspace(-1.6,   0.,    5)
    # binsx = np.logspace(-7,2,40)
    # binsx = np.arange(0.,200.,10.)


    MeasurementRegion = Selections.Region('cr','mmm','CustomRegion')

    ht = dataframe\
        .Define('abs_l1_eta','abs(l1_eta)')\
        .Define('abs_l1_dxy','abs(l1_dxy)')\
        .Define('abs_l1_dz','abs(l1_dz)')\
        .Filter(MeasurementRegion.data)\
        .Histo1D(('','',len(binsx)-1,binsx),'%s'%varName)

    hl = dataframe\
        .Define('abs_l1_eta','abs(l1_eta)')\
        .Define('abs_l1_dxy','abs(l1_dxy)')\
        .Define('abs_l1_dz','abs(l1_dz)')\
        .Filter(MeasurementRegion.baseline)\
        .Histo1D(('','',len(binsx)-1,binsx),'%s'%varName)

    hist_tight = ht.Clone()
    hist_loose = hl.Clone()

    if varName == 'l1_pt':  hist_tight.SetTitle(';lepton p_{T} (GeV); fakerate')
    if varName == 'abs_l1_eta': hist_tight.SetTitle(';lepton #eta; fakerate')
    if varName == 'abs_l1_dxy': hist_tight.SetTitle(';lepton impact parameter d_{xy} (cm); fakerate')
    if varName == 'abs_l1_dz': hist_tight.SetTitle(';lepton impact parameter d_{z} (cm); fakerate')
    if varName == 'hnl_2d_disp': hist_tight.SetTitle('; 2D displacement (cm); fakerate')
    if varName == 'hnl_dr_12': hist_tight.SetTitle('; #Delta R_{12}; fakerate')
    if varName == 'hnl_m_12': hist_tight.SetTitle('; dilepton invariant mass m_{12} (GeV); fakerate')
    if varName == 'sv_prob': hist_tight.SetTitle('; dilepton vertex quality; fakerate')
    if varName == 'hnl_w_vis_m': hist_tight.SetTitle('; Tri-Lepton Mass (GeV); fakerate')
    
    

    hist_tight.Divide(hist_loose)

    hist_tight.SetMarkerColor(ROOT.kBlue+2)
    hist_tight.SetLineColor(ROOT.kBlue+2)
    hist_tight.GetYaxis().SetRangeUser(0.,0.40)
    hist_tight.Draw()

    if varName == 'hnl_2d_disp': can.SetLogx()
    if varName == 'hnl_dr_12': can.SetLogx()
    if varName == 'abs_l1_dz': can.SetLogx()
    # if varName == 'sv_prob': can.SetLogx()
    # can.SetLogy()

    plotfactory.showlumi('59.7 fb^{-1} (13 TeV)')
    plotfactory.showlogopreliminary()

    can.Update()
    plotName = 'fr_%s'%varName
    for datatype in ['pdf','png','tex','root']:
        can.SaveAs('fakerateplots/%s/%s.%s'%(datatype,plotName,datatype))

    for histogram in [ht, hl, hist_tight, hist_loose]:
        histogram.Reset()
        
if __name__ == '__main__':
    varNames = []

    # varNames.append('l1_pt')
    # varNames.append('abs_l1_eta')
    # varNames.append('abs_l1_dxy')
    # varNames.append('abs_l1_dz')
    # varNames.append('hnl_2d_disp')
    # varNames.append('hnl_dr_12')
    # varNames.append('hnl_m_12')
    # varNames.append('sv_prob')
    varNames.append('hnl_w_vis_m')
    
    for varName in varNames:
        makeFakeRatePlot(varName)

