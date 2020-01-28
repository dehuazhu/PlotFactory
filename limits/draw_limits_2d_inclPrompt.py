#!/usr/bin/env python
from os import environ as env
import ROOT as rt
from collections import OrderedDict
import re
from pdb import set_trace
import numpy as np
from matplotlib import pyplot as plt
# import shapely.geometry as sg
import os
# from termcolor import colored
import plotfactory    

def makeDelphiDisplaced():
    masses = np.array([10.0**-0.365297, 10.0**-0.228311, 10.0**-0.125571, 10.0**-0.020548, 10.0**0.095890, 10.0**0.232877, 10.0**0.315068, 10.0**0.326484, 10.0**0.363014,10.0**0.413242, 10.0**0.461187, 10.0**0.506849, 10.0**0.552511, 10.0**0.586758, 10.0**0.609589, 10.0**0.618721, 10.0**0.625571, 10.0**0.632420, 10.0**0.639269, 10.0**0.646119, 10.0**0.655251, 10.0**0.655251])
    exp = np.array([10.0**-2.000000, 10.0**-2.467626, 10.0**-2.827338, 10.0**-3.172662, 10.0**-3.561151, 10.0**-3.978417, 10.0**-4.215827, 10.0**-4.237410, 10.0**-4.323741, 10.0**-4.460432, 10.0**-4.582734, 10.0**-4.661871, 10.0**-4.712230, 10.0**-4.669065, 10.0**-4.503597, 10.0**-4.309353, 10.0**-4.079137, 10.0**-3.769784, 10.0**-3.431655, 10.0**-3.158273, 10.0**-2.985612, 10.0**-2.985612])

    gr_exp = rt.TGraph(len(masses), masses, exp)
    return gr_exp 

def makeDelphiPrompt():
    masses = np.array([10.0**0.292237442922374, 10.0**0.342465753424657, 10.0**0.390410958904109, 10.0**0.447488584474885, 10.0**0.481735159817351, 10.0**0.534246575342466, 10.0**0.591324200913242, 10.0**0.625570776255707, 10.0**0.652968036529680, 10.0**0.694063926940639, 10**0.732876712328766, 10**0.776255707762557, 10**0.815068493150685, 10**0.860730593607306, 10**0.915525114155251, 10**0.972602739726027, 10**1.038812785388127, 10**1.098173515981735, 10**1.166666666666666, 10**1.230593607305935, 10**1.280821917808219, 10**1.331050228310502, 10**1.381278538812785, 10**1.456621004566209, 10**1.513698630136986, 10**1.5867579908, 10**1.630136986301369, 10**1.666666666666666, 10**1.712328767123287, 10**1.751141552511415, 10**1.785388127853881, 10**1.815068493150684, 10**1.837899543378995, 10**1.856164383561643, 10**1.872146118721461, 10**1.888127853881278, 10**1.901826484018265])
    exp = np.array([10**-2.19424460431654, 10**-2.49640287769784, 10**-2.78417266187050, 10**-3.11510791366906, 10**-3.33812949640287, 10**-3.63309352517985, 10**-3.95683453237410, 10**-4.14388489208633, 10**-4.30935251798561, 10**-4.47482014388489, 10**-4.59712230215827, 10**-4.68345323741007, 10**-4.72661870503597, 10**-4.75539568345323, 10**-4.74820143884892, 10**-4.73381294964028, 10**-4.72661870503597, 10**-4.72661870503597, 10** -4.70503597122302, 10**-4.68345323741007, 10**-4.67625899280575, 10**-4.66187050359712, 10**-4.63309352517985, 10**-4.60431654676259, 10**-4.60431654676259, 10**-4.60431654676259, 10**-4.59712230215827, 10**-4.56115107913669, 10**-4.48920863309352, 10**-4.38129496402877, 10**-4.20143884892086, 10**-3.98561151079136, 10**-3.73381294964028, 10**-3.50359712230215, 10**-3.20863309352517, 10**-2.92805755395683, 10**-2.64748201438848])
    gr_exp = rt.TGraph(len(masses), masses, exp)
    return gr_exp 

def makeAtlasDisplacedMuonLNV():
    # masses = np.array([4.1, 4.2, 4.4, 4.6, 5.2, 5.8, 6.0, 6.6, 6.8, 7.4, 7.8, 8.0, 8.1, 8.1, 7.8, 7.5, 7.0, 6.0 , 5.6, 5.2, 4.8, 4.4, 4.2])
    # exp = np.array([2e-4, 4e-4, 5e-4, 4e-4, 2e-4, 1e-4, 8e-5, 4e-5, 3e-5, 1.3e-5, 8e-6, 5.3e-6, 3.5e-6, 2.5e-6, 2e-6, 1.9e-6, 2e-6, 3.1e-6, 4e-6, 6e-6, 1e-5, 2.3e-5, 4.3e-5])
    masses = np.array([8.1, 7.8, 7.5, 7.0, 6.0 , 5.6, 5.2, 4.8, 4.4, 4.2])
    exp = np.array([2.5e-6, 2e-6, 1.9e-6, 2e-6, 3.1e-6, 4e-6, 6e-6, 1e-5, 2.3e-5, 4.3e-5])
    gr_exp = rt.TGraph(len(masses), masses, exp)
    return gr_exp 

def makeAtlasDisplacedMuonLNC():
    # masses = np.array([4.1, 4.2, 4.4, 4.6, 5.2, 5.8, 6.0, 6.6, 6.8, 7.4, 7.8, 8.0, 8.1, 8.1, 7.8, 7.5, 7.0, 6.0 , 5.6, 5.2, 4.8, 4.4, 4.2])
    # exp = np.array([2e-4, 4e-4, 5e-4, 4e-4, 2e-4, 1e-4, 8e-5, 4e-5, 3e-5, 1.3e-5, 8e-6, 5.3e-6, 3.5e-6, 2.5e-6, 2e-6, 1.9e-6, 2e-6, 3.1e-6, 4e-6, 6e-6, 1e-5, 2.3e-5, 4.3e-5])
    masses = np.array([9.6, 9.2, 8.8, 8.0, 7.0, 6.0, 5.0, 4.2, 4.1])
    exp = np.array([2.3e-6, 1.6e-6, 1.4e-6, 1.5e-6, 2e-6, 3.3e-6, 8e-6, 5e-5, 1e-4])
    gr_exp = rt.TGraph(len(masses), masses, exp)
    return gr_exp 



def draw_limits2DWithPrompt(ExclusionLimits2D_low, ExclusionLimits2D_high, input_file, output_dir, ch='mmm', twoD=False, verbose=False): 
    '''
    #############################################################################
    ## producing coupling vs r limits for each signal mass and a given channel ##
    ## also has the option 2D, in order to draw mass vs coupling limits (this  ## 
    ## uses the intersections of the 1D limits and the r=1 line)               ##
    #############################################################################
    '''

    # promptMuonDirectory     = '/Users/dehuazhu/SynologyDrive/PhD/7_Writing/1912_AnalysisNote_HNL/AN-19-272/1_Sections/6_Interpretation/figures/Limits/limitsMuonMixing.root'
    promptMuonDirectory     = '/work/dezhu/3_figures/2_Limits/PromptAnalysis/limitsMuonMixing.root'
    promptMuonFile = rt.TFile(promptMuonDirectory)
    promptMuonGraph_ep2 = promptMuonFile.Get('expected_2sigmaUp')
    promptMuonGraph_ep1 = promptMuonFile.Get('expected_1sigmaUp')
    promptMuonGraph_exp = promptMuonFile.Get('expected_central')
    promptMuonGraph_em1 = promptMuonFile.Get('expected_1sigmaDown')
    promptMuonGraph_em2 = promptMuonFile.Get('expected_2sigmaDown')

    # promptElectronDirectory = '/Users/dehuazhu/SynologyDrive/PhD/7_Writing/1912_AnalysisNote_HNL/AN-19-272/1_Sections/6_Interpretation/figures/Limits/limitsElectronMixing.root'
    promptElectronDirectory = '/work/dezhu/3_figures/2_Limits/PromptAnalysis/limitsElectronMixing.root'
    promptElectronFile = rt.TFile(promptElectronDirectory)
    promptElectronGraph_ep2 = promptMuonFile.Get('expected_2sigmaUp')
    promptElectronGraph_ep1 = promptMuonFile.Get('expected_1sigmaUp')
    promptElectronGraph_exp = promptMuonFile.Get('expected_central')
    promptElectronGraph_em1 = promptMuonFile.Get('expected_1sigmaDown')
    promptElectronGraph_em2 = promptMuonFile.Get('expected_2sigmaDown')


    low_masses  = ExclusionLimits2D_low['masses']
    low_x_err   = ExclusionLimits2D_low['x_err'] 
    low_y_exp   = ExclusionLimits2D_low['y_exp'] 
    low_y_ep1s  = ExclusionLimits2D_low['y_ep1s']
    low_y_ep2s  = ExclusionLimits2D_low['y_ep2s']
    low_y_em1s  = ExclusionLimits2D_low['y_em1s']
    low_y_em2s  = ExclusionLimits2D_low['y_em2s']

    high_masses = ExclusionLimits2D_high['masses']
    high_x_err  = ExclusionLimits2D_high['x_err'] 
    high_y_exp  = ExclusionLimits2D_high['y_exp'] 
    high_y_ep1s = ExclusionLimits2D_high['y_ep1s']
    high_y_ep2s = ExclusionLimits2D_high['y_ep2s']
    high_y_em1s = ExclusionLimits2D_high['y_em1s']
    high_y_em2s = ExclusionLimits2D_high['y_em2s']

    low_exp = rt.TGraph           (len(low_masses), np.array(low_masses), np.array(low_y_exp))
    low_gr1 = rt.TGraphAsymmErrors(len(low_masses), np.array(low_masses), np.array(low_y_exp), np.array(low_x_err), np.array(low_x_err), np.array(low_y_em1s), np.array(low_y_ep1s))
    low_gr2 = rt.TGraphAsymmErrors(len(low_masses), np.array(low_masses), np.array(low_y_exp), np.array(low_x_err), np.array(low_x_err), np.array(low_y_em2s), np.array(low_y_ep2s))
    
    high_exp = rt.TGraph           (len(high_masses), np.array(high_masses), np.array(high_y_exp))
    high_gr1 = rt.TGraphAsymmErrors(len(high_masses), np.array(high_masses), np.array(high_y_exp), np.array(high_x_err), np.array(high_x_err), np.array(high_y_em1s), np.array(high_y_ep1s))
    high_gr2 = rt.TGraphAsymmErrors(len(high_masses), np.array(high_masses), np.array(high_y_exp), np.array(high_x_err), np.array(high_x_err), np.array(high_y_em2s), np.array(high_y_ep2s))
    
    rt.gStyle.SetOptStat(0000)

    # B_X  = np.logspace(0,2.5,10,base=10)
    # B_X  = np.logspace(0.,1.,10)
    B_X  = np.array([1.,2.,3.,4.,5.,6.,7.,8.,9.,10.])
    # B_Y  = np.logspace(-6.7, -1, 10, base=10)
    B_Y  = np.logspace(-5.9, -1, 10, base=10)
    framer = rt.TH2F('framer', 'framer', len(B_X)-1, B_X, len(B_Y)-1, B_Y)
    # framer.GetXaxis().SetRangeUser(1, 10.)
    framer.GetXaxis().SetRangeUser(1, 8.)
    framer.GetYaxis().SetRangeUser(1e-12,1e-1)

    if ch == 'mmm': 
        framer.SetTitle('#mu#mu#mu; m_{N}(GeV); |V_{N#mu N}|^{2}' )
    if ch == 'eee':
        framer.SetTitle('eee; m_{N}(GeV); |V_{e N}|^{2}' )
    if ch == 'mem_OS':
        framer.SetTitle('#mu#mue OS; m_{N}(GeV); |V_{#mu N}|^{2}' )
    if ch == 'mem_SS':
        framer.SetTitle('#mu#mue SS; m_{N}(GeV); |V_{#mu N}|^{2}' )
    if ch == 'eem_OS':
        framer.SetTitle('ee#mu OS; m_{N}(GeV); |V_{e N}|^{2}' )
    if ch == 'eem_SS':
        framer.SetTitle('ee#mu SS; m_{N}(GeV); |V_{e N}|^{2}' )

    low_exp.SetMarkerStyle(22)
    low_exp.SetMarkerSize(1)
    low_exp.SetMarkerColor(rt.kBlack)
    low_exp.SetLineColor(rt.kBlack)
    low_exp.SetLineWidth(2)

    low_gr1.SetFillColor(rt.kGreen+1)
    low_gr1.SetLineColor(rt.kGreen+1)
    low_gr1.SetLineWidth(2)

    low_gr2.SetFillColor(rt.kOrange)
    low_gr2.SetLineColor(rt.kOrange)
    low_gr2.SetLineWidth(2)

    high_exp.SetMarkerStyle(22)
    high_exp.SetMarkerSize(1)
    high_exp.SetMarkerColor(rt.kBlack)
    high_exp.SetLineColor(rt.kBlack)
    high_exp.SetLineWidth(2)

    high_gr1.SetFillColor(rt.kGreen+1)
    high_gr1.SetLineColor(rt.kGreen+1)
    high_gr1.SetLineWidth(2)

    high_gr2.SetFillColor(rt.kOrange)
    high_gr2.SetLineColor(rt.kOrange)
    high_gr2.SetLineWidth(2)

    for graph in [promptMuonGraph_ep2, promptElectronGraph_ep2, promptMuonGraph_em2, promptElectronGraph_em2]:
        graph.SetFillColor(rt.kAzure+6)
        graph.SetLineColor(rt.kAzure+6)
        graph.SetLineStyle(2)
        graph.SetLineWidth(2)

    for graph in [promptMuonGraph_ep1, promptElectronGraph_ep1, promptMuonGraph_em1, promptElectronGraph_em1]:
        graph.SetFillColor(rt.kAzure+1)
        graph.SetLineColor(rt.kAzure+1)
        graph.SetLineStyle(7)
        graph.SetLineWidth(2)

    for graph in [promptMuonGraph_exp, promptElectronGraph_exp]:
        graph.SetMarkerStyle(22)
        graph.SetMarkerSize(1)
        graph.SetMarkerColor(rt.kAzure+2)
        graph.SetLineColor(  rt.kAzure+2)
        graph.SetLineStyle(1)
        graph.SetLineWidth(2)

    can = rt.TCanvas('limits', 'limits',700,530)
    # can = rt.TCanvas('limits', 'limits')
    can.cd() 
    can.SetLogy() 
    # can.SetLogx()

    if ch == 'mCombined':
        framer.GetYaxis().SetTitle('|V_{N#mu}|^{2}')
    if ch == 'eCombined':
        framer.GetYaxis().SetTitle('|V_{Ne}|^{2}')

    framer.GetYaxis().SetTitleOffset(1.5)
    framer.GetXaxis().SetTitle('m_{N} (GeV)')
    framer.GetXaxis().SetTitleOffset(1.5)
    framer.Draw()

    # low_gr2.Draw('same, E1')
    low_gr2.Draw('same, E3')
    # low_gr1.Draw('same, E1')
    low_gr1.Draw('same, E3')
    # low_exp.Draw('same, LP')
    low_exp.Draw('same, L')

    DelphiDisplaced_exp =  makeDelphiDisplaced()
    DelphiPrompt_exp =  makeDelphiPrompt()
    AtlasDisplacedMuonLNV_exp = makeAtlasDisplacedMuonLNV()
    AtlasDisplacedMuonLNC_exp = makeAtlasDisplacedMuonLNV()

    for graph in [DelphiDisplaced_exp, DelphiPrompt_exp, AtlasDisplacedMuonLNV_exp, AtlasDisplacedMuonLNC_exp]:
        graph.SetMarkerStyle(0)
        graph.SetMarkerSize(1)
        graph.SetLineStyle(1)
        graph.SetLineWidth(2)

        DelphiDisplaced_exp.SetMarkerColor(rt.kOrange+2)
        DelphiDisplaced_exp.SetLineColor(  rt.kOrange+2)

        DelphiPrompt_exp.SetMarkerColor(rt.kOrange+2)
        DelphiPrompt_exp.SetLineColor(  rt.kOrange+2)
        DelphiPrompt_exp.SetLineStyle(2)

        AtlasDisplacedMuonLNV_exp.SetMarkerColor(rt.kPink+10)
        AtlasDisplacedMuonLNV_exp.SetLineColor(  rt.kPink+10)

    if ch == 'mCombined': 
        promptMuonGraph_ep2.Draw('same, L')
        promptMuonGraph_ep1.Draw('same, L')
        promptMuonGraph_exp.Draw('same, L')
        promptMuonGraph_em1.Draw('same, L')
        promptMuonGraph_em2.Draw('same, L')

        DelphiDisplaced_exp.Draw('same, L')
        DelphiPrompt_exp.Draw('same, L')
        AtlasDisplacedMuonLNV_exp.Draw('same, L')
        # AtlasDisplacedMuonLNC_exp.Draw('same, L')
    
    
    if ch == 'eCombined': 
        promptElectronGraph_exp.Draw('same, L')
        promptElectronGraph_ep1.Draw('same, L')
        promptElectronGraph_exp.Draw('same, L')
        promptElectronGraph_em1.Draw('same, L')
        promptElectronGraph_em2.Draw('same, L')

    # leg = rt.TLegend(.4,.75,.8,.88)
    leg = rt.TLegend(.53,.58,.80,.88)
    leg.SetBorderSize(0)
    leg.AddEntry(low_exp, 'Expected', 'L')
    leg.AddEntry(low_gr1, 'Expected #pm 1 #sigma', 'CFL')
    leg.AddEntry(low_gr2, 'Expected #pm 2 #sigma', 'CFL')
    leg.AddEntry(promptMuonGraph_exp, 'CMS [EXO-17-012]', 'L')
    leg.AddEntry(DelphiDisplaced_exp, 'DELPHI long-lived')
    leg.AddEntry(DelphiPrompt_exp, 'DELPHI prompt')
    leg.AddEntry(AtlasDisplacedMuonLNV_exp, 'ATLAS')

    # leg.AddEntry(AtlasDisplacedMuonLNV_exp, 'ATLAS LNV')
    # leg.AddEntry(AtlasDisplacedMuonLNC_exp, 'ATLAS LNC')
    leg.Draw('apez same')


    
    plotfactory.showlogopreliminary()
    # plotfactory.showlumi('N#rightarrow%s;  59.7 fb^{-1}  (13 TeV)'%(ch))
    plotfactory.showlumi('59.7 fb^{-1}  (13 TeV)')
    can.Update()

    if not os.path.isdir(output_dir + 'pdf'): os.mkdir(output_dir + 'pdf')
    if not os.path.isdir(output_dir + 'png'): os.mkdir(output_dir + 'png')
    if not os.path.isdir(output_dir + 'root'): os.mkdir(output_dir + 'root')
    if not os.path.isdir(output_dir + 'tex'): os.mkdir(output_dir + 'tex')

    can.SaveAs(output_dir + 'pdf/%s.pdf' %(ch))
    can.SaveAs(output_dir + 'png/%s.png' %(ch))
    can.SaveAs(output_dir + 'root/%s.root' %(ch))
    can.SaveAs(output_dir + 'tex/%s.tex' %(ch))

if __name__ == '__main__':
    print('starting draw_limits.py...')
    
    plotfactory.setpfstyle()

    channel = 'mmm'
    # channel = 'mem_OS'
    # channel = 'mem_SS'
    # channel = 'eee'
    # channel = 'eem_OS'
    # channel = 'eem_SS'

    #2017
    # base_dir   = '/work/dezhu/3_figures/2_Limits/2017/mmm/20191119_limits'

    #2018
    # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191120_Aachen'%channel
    # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191121_RiccardoDatacards'%channel
    # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweight'%channel
    # base_dir   = '/Users/dehuazhu/SynologyDrive/PhD/7_Writing/1912_AnalysisNote_HNL/AN-19-272/1_Sections/6_Interpretation/figures/Limits/%s/20191129_NewDispBin'%channel
    input_file = base_dir + '/output.txt'

    output_dir = base_dir + '/output/' 
    if not os.path.isdir(output_dir): os.mkdir(output_dir)

    draw_limits2D(input_file, output_dir, ch = channel)
