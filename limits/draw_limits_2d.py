#!/usr/bin/env python
from os import environ as env
import ROOT as rt
from collections import OrderedDict
import re
from pdb import set_trace
import numpy as np
from matplotlib import pyplot as plt
import shapely.geometry as sg
import os
from termcolor import colored
import plotfactory    



def draw_limits(input_file, output_dir, ch='mmm', twoD=False, verbose=False): 
    '''
    #############################################################################
    ## producing coupling vs r limits for each signal mass and a given channel ##
    ## also has the option 2D, in order to draw mass vs coupling limits (this  ## 
    ## uses the intersections of the 1D limits and the r=1 line)               ##
    #############################################################################
    '''

    
    masses = [1.,2.,3.,4.,5.,6.,8.,10.,20.]
    x_err  = np.zeros(len(masses))

    # y_exp  = [2e-4,2.5e-6,2e-7,3e-8,8e-9  ,4e-9,7e-10 ,4e-10,7e-9]
    # y_ep1s = [3e-4,6e-6  ,3e-7,5e-8,0.5e-8,6e-9,9e-10 ,6e-10,1e-8]
    # y_ep2s = [7e-4,8e-6  ,7e-7,8e-8,2e-8  ,9e-9,0.5e-9,1e-9 ,2e-8] 
    # y_em1s = [1e-4,0.5e-6,1e-7,2e-8,5e-9  ,2e-9,4e-10 ,2e-10,3e-9]
    # y_em2s = [6e-5,9e-7  ,8e-8,1e-8,3e-9  ,1e-9,2e-10 ,1e-10,1e-9]

    y_exp  = [2e-4  ,2.5e-6,2e-7  ,3e-8,8e-9 ,4e-9,7e-10 ,4e-10,7e-9 ]
    y_ep1s = [1e-4  ,3.5e-6,1e-7  ,2e-8,7e-9 ,2e-9,2e-10 ,2e-10,3e-9 ]
    y_ep2s = [5e-4  ,5.5e-6,6e-7  ,5e-8,12e-9,5e-9,8e-10 ,6e-10,8e-9] 
    y_em1s = [1e-4  ,0.5e-6,1e-7  ,1e-8,3e-9 ,2e-9,3e-10 ,2e-10,4e-9 ]
    y_em2s = [1.4e-4,1.1e-6,1.2e-7,2e-8,5e-9 ,3e-9,5e-10 ,3e-10,6e-9 ]

    exp = rt.TGraph           (len(masses), np.array(masses), np.array(y_exp))
    gr1 = rt.TGraphAsymmErrors(len(masses), np.array(masses), np.array(y_exp), np.array(x_err), np.array(x_err), np.array(y_em1s), np.array(y_ep1s))
    gr2 = rt.TGraphAsymmErrors(len(masses), np.array(masses), np.array(y_exp), np.array(x_err), np.array(x_err), np.array(y_em2s), np.array(y_ep2s))
    
    rt.gStyle.SetOptStat(0000)
    B_X  = np.logspace(-0.1,2.3,10,base=10)
    B_Y  = np.logspace(-11, 0, 10, base=10)
    framer = rt.TH2F('framer', 'framer', len(B_X)-1, B_X, len(B_Y)-1, B_Y)
    framer.GetYaxis().SetRangeUser(1e-11,1)
    framer.GetXaxis().SetRangeUser(0, 21)

    if ch == 'mmm': 
        framer.SetTitle('#mu#mu#mu; m_{N}(GeV); |V_{#mu N}|^{2}' )
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

    exp.SetMarkerStyle(22)
    exp.SetMarkerSize(1)
    exp.SetMarkerColor(rt.kRed+2)
    exp.SetLineColor(rt.kRed+2)

    gr1.SetFillColor(rt.kGreen+2)
    gr1.SetLineColor(rt.kGreen+2)
    gr1.SetLineWidth(2)

    gr2.SetFillColor(rt.kOrange)
    gr2.SetLineColor(rt.kOrange)
    gr2.SetLineWidth(2)

    can = rt.TCanvas('limits', 'limits')
    can.cd() 
    can.SetLogy() 
    can.SetLogx()

    framer.Draw()
    can.Update()
    gr2.Draw('same, E1')
    gr2.Draw('same, E3')
    can.Update()
    gr1.Draw('same, E1')
    gr1.Draw('same, E3')
    can.Update()
    exp.Draw('same, LP')
    can.Update()

    leg = rt.TLegend(.4,.75,.8,.88)
    leg.AddEntry(exp, 'Expected', 'LP')
    leg.AddEntry(gr1, 'Expected #pm 1 #sigma', 'E3')
    leg.AddEntry(gr2, 'Expected #pm 2 #sigma', 'E3')
    leg.Draw('apez same')

    
    # plotfactory.showlogopreliminary()
    plotfactory.showlumi('N#rightarrow%s;  59.7 fb^{-1}  (13 TeV)'%(ch))
    can.Update()

    if not os.path.isdir(output_dir + 'pdf'): os.mkdir(output_dir + 'pdf')
    if not os.path.isdir(output_dir + 'png'): os.mkdir(output_dir + 'png')
    if not os.path.isdir(output_dir + 'root'): os.mkdir(output_dir + 'root')

    can.SaveAs(output_dir + 'pdf/%s.pdf' %(ch))
    can.SaveAs(output_dir + 'png/%s.png' %(ch))
    can.SaveAs(output_dir + 'root/%s.root' %(ch))
    set_trace()

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
    base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweight'%channel
    input_file = base_dir + '/output.txt'

    output_dir = base_dir + '/output/' 
    if not os.path.isdir(output_dir): os.mkdir(output_dir)

    draw_limits(input_file, output_dir, ch = channel)
