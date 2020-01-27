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



# def draw_limits2D(input_file, output_dir, ch='mmm', twoD=False, verbose=False): 
# def draw_limits2D(masses, x_err, y_exp, y_ep1s, y_ep2s, y_em1s, y_em2s, input_file, output_dir, ch='mmm', twoD=False, verbose=False): 
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

    # B_X  = np.logspace(-0.1,1,50,base=10)
    # B_Y  = np.logspace(-11, 2, 50, base=10)
    # framer = rt.TH2F('framer', 'framer', len(B_X)-1, B_X, len(B_Y)-1, B_Y)
    # framer.GetXaxis().SetRangeUser(0, 10)
    # framer.GetYaxis().SetRangeUser(1e-7,1)

    # B_X  = np.logspace(-0.1,3,10,base=10)
    # B_Y  = np.logspace(-11, 2, 10, base=10)
    # framer = rt.TH2F('framer', 'framer', len(B_X)-1, B_X, len(B_Y)-1, B_Y)
    # framer.GetXaxis().SetRangeUser(1, 40)
    # framer.GetYaxis().SetRangeUser(1e-7,1)

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

    # high_gr2.Draw('same, E1')
    # high_gr2.Draw('same, E3')
    # high_gr1.Draw('same, E1')
    # high_gr1.Draw('same, E3')
    # high_exp.Draw('same, LP')
    # high_exp.Draw('same, L')

    if ch == 'mCombined': 
        promptMuonGraph_ep2.Draw('same, L')
        promptMuonGraph_ep1.Draw('same, L')
        promptMuonGraph_exp.Draw('same, L')
        promptMuonGraph_em1.Draw('same, L')
        promptMuonGraph_em2.Draw('same, L')
    
    if ch == 'eCombined': 
        promptElectronGraph_exp.Draw('same, L')
        promptElectronGraph_ep1.Draw('same, L')
        promptElectronGraph_exp.Draw('same, L')
        promptElectronGraph_em1.Draw('same, L')
        promptElectronGraph_em2.Draw('same, L')

    # leg = rt.TLegend(.4,.75,.8,.88)
    leg = rt.TLegend(.46,.58,.80,.79)
    leg.SetBorderSize(0)
    leg.AddEntry(low_exp, 'Expected', 'L')
    leg.AddEntry(low_gr1, 'Expected #pm 1 #sigma', 'CFL')
    leg.AddEntry(low_gr2, 'Expected #pm 2 #sigma', 'CFL')
    leg.AddEntry(promptMuonGraph_exp, 'CMS [EXO-17-012]', 'L')
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
