'''
###############################################################################
## IN ORDER TO RUN THIS CODE EXECUTE:                                        ##
## (FOR RUNNING THE DIFFERENT SCRIPTS ALWAYS START A NEW BASH SESSION)       ##
## source /cvmfs/sft.cern.ch/lcg/views/LCG_94/x86_64-slc6-gcc8-opt/setup.sh  ##
## (THE shapely.geometry PACKAGE NEEDS A NEWER python VERSION)               ##
## THEN RUN: draw_signals(CH), WHERE CH = 'mmm', eem_OS', ...                ##
###############################################################################
'''
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
from socket import gethostname
from draw_limits_2d import draw_limits2D
from draw_limits_2d_inclPrompt import draw_limits2DWithPrompt
from intersection import intersection


def get_signals(verbose=False):
    '''
    ###################################
    ## preparing a signal dictionary ##
    ###################################
    '''
    # read input
    with open('signals2.py', 'r') as f_in:
        array = []
        for line in f_in:
            array.append(line)

    # reorganize lines to each signal
    signals = OrderedDict()

    Mass = None; V = None
    for line in array:


        mode = None
        if '_e_' in line:   mode = 'e'  
        if '_mu_' in line:  mode = 'mu' 
        if '_tau_' in line: mode = 'tau'

        if 'Dirac' in line: continue


        line = line.strip()
        line = re.sub('HN3L_', '', line)
        line = re.sub('_massiveAndCKM_LO', '', line)
        line = re.sub('_', '', line)
        line = re.sub(' ', '', line)
        if line == '': continue

        mass = re.sub('V.*', '', line)
        mass = re.sub('M', '', mass)
        if mode is 'e'   : v   = re.sub('e.*', '', line)
        if mode is 'mu'  :v    = re.sub('mu.*', '', line)
        if mode is 'tau' :v    = re.sub('tau.*', '', line)
        v    = re.sub('p', '.', v)
        # v    = re.sub('M.V', '', v)
        v    = re.sub('.*V', '', v)
        Mass, V = mass, v


        try: signals['M' + Mass + '_V' + V + '_' + mode]['mass'] = float(mass)
        except:
            signals['M' + Mass + '_V' + V + '_' + mode] = OrderedDict()
            signals['M' + Mass + '_V' + V + '_' + mode]['mass'] = float(mass)


        # V2 = None
        if 'v2=' in line: 
            V2 = None
            V2 = re.sub('.*v2=', '', line) 
            signals['M' + Mass + '_V' + V + '_' + mode]['V2'] = float(V2)
            if verbose: print (V2, float(V)**2)

        # xsec = None
        if 'xs=' in line: 
            xsec = None
            xsec = re.sub('.*xs=', '', line) 
            signals['M' + Mass + '_V' + V + '_' + mode]['xsec'] = float(xsec)

        # xsec_err = None
        if 'xse=' in line: 
            xsec_err = None
            xsec_err = re.sub('.*xse=', '', line) 
            signals['M' + Mass + '_V' + V + '_' + mode]['xsec_err'] = float(xsec_err)

    if verbose:
        for k in signals.keys(): 
            for kk in signals[k].keys():
                print (k, kk, signals[k][kk])
            print ('\n')
    
    return signals

def get_lim_dict(input_file, output_dir, ch='mem', verbose=False):
    '''
    #####################################
    ## preparing the limits dictionary ##
    ## from the output file that       ##
    ## combine is piped to             ## 
    #####################################
    '''
    # in_file = '/t3home/vstampf/eos/plots/limits/inputs/data_cards_aug_20/limits_aug_20_%s.txt' %ch
    env['LIM_FILE']   = input_file
    # env['OUT_FOLDER'] = '/t3home/vstampf/eos/plots/limits/outputs/'
    env['OUT_FOLDER'] = output_dir
    with open(input_file, 'r') as f_in:
        array = []
        for line in f_in:
            array.append(line)

    # reorganize lines to each signal
    lim_dict = OrderedDict()
    masses = []

    Mass = None; V = None; mode = None
    for line in array:
        line = line.strip()
        if line == '': continue

        mode = None

        if ((ch == 'mmm') or (ch == 'mem_OS') or (ch == 'mem_SS') or (ch == 'mCombined')): mode = 'mu'
        if ((ch == 'eee') or (ch == 'eem_OS') or (ch == 'eem_SS') or (ch == 'eCombined')): mode = 'e'


        # if '_e_' in line:   mode = 'e'  
        # elif '_mu_' in line:  mode = 'mu' 
        # elif '_tau_' in line: mode = 'tau'

        if ('HNL' in line) or ('hnl' in line):
            if '.root' in line: continue
            # mass = re.sub(r'.*M([0-9])_V.*',r'\1', line)
            mass = re.sub('.*_M','',line)
            mass = re.sub('_.*','',mass)
            v    = re.sub('.*Vp', '', line)
            v    = re.sub('_.*', '', v)
            v    = '0.' + v
            Mass, V = mass, v
            try:
                massNumber = int(Mass)
                if massNumber not in masses:
                    masses.append(massNumber) 
            except: pass

            try: 
                lim_dict['M' + Mass + '_V' + V + '_' + mode] = OrderedDict()
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['mass'] = float(Mass)
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['V']    = float(V)
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['V2']   = float(V)**2
            except: set_trace()

        ep1s = None; ep2s = None; em1s = None; em2s = None; om1s = None; op1s = None; obs = None; exp = None
        line = re.sub(' ', '', line)


        try:
            if 'Observed'     in line: 
                obs  = re.sub('.*r<', '', line) 
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['obs']  = float(obs)

            if 'Expected2.5'  in line:                           
                em2s = re.sub('.*r<', '', line)                  
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['em2s'] = float(em2s)

            if 'Expected16.0' in line:                           
                em1s = re.sub('.*r<', '', line)                  
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['em1s'] = float(em1s)

            if 'Expected50.0' in line:                           
                exp  = re.sub('.*r<', '', line)                  
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['exp']  = float(exp)

            if 'Expected84.0' in line:                           
                ep1s = re.sub('.*r<', '', line)                  
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['ep1s'] = float(ep1s)

            if 'Expected97.5' in line:                           
                ep2s = re.sub('.*r<', '', line)                 
                lim_dict['M' + Mass + '_V' + V + '_' + mode]['ep2s'] = float(ep2s)
        except: set_trace()

    if verbose:
        for k in lim_dict.keys(): 
            for kk in lim_dict[k].keys():
                print (k, kk, lim_dict[k][kk])
            print ('\n')

    masses = sorted(masses)
    return lim_dict, masses

def draw_limits(input_file, output_dir, ch='mmm', twoD=False, verbose=False): 
    '''
    #############################################################################
    ## producing coupling vs r limits for each signal mass and a given channel ##
    ## also has the option 2D, in order to draw mass vs coupling limits (this  ## 
    ## uses the intersections of the 1D limits and the r=1 line)               ##
    #############################################################################
    '''
    # create signal and limits dictionary
    limits, masses  = get_lim_dict(input_file, output_dir, ch=ch)
    signals = get_signals()

    b     = np.arange(0., 11, 1)
    req1  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    ixs = OrderedDict()

    #sort the dictionary after v values
    limits = OrderedDict(sorted(limits.items(),key=lambda t: t[1]['V']))

    ExclusionLimits2D_low  = {}
    ExclusionLimits2D_high = {}
    for ExclusionLimits2D in [ExclusionLimits2D_low,ExclusionLimits2D_high]:
        ExclusionLimits2D['masses'] = []
        ExclusionLimits2D['x_err']  = []
        ExclusionLimits2D['y_exp']  = []
        ExclusionLimits2D['y_ep1s'] = []
        ExclusionLimits2D['y_ep2s'] = []
        ExclusionLimits2D['y_em1s'] = []
        ExclusionLimits2D['y_em2s'] = []

    for mass in masses:
    # for m in [1,2,3,4,5,6,7,8,9,10]:
        # print(colored('doing MASS = %d GeV'%mass,'green'))
        print('### doing MASS = %d GeV'%mass)

        y_exp = []; y_ep1s = []; y_ep2s = []; y_em2s = []; y_em1s = [];  
        v2s   = [lim for lim in limits if 'M%d_' %mass in lim]
        b_V2  = [] 
        for v2 in v2s:
            # if limits[v2].has_key('exp'):  
            if 'exp' in limits[v2]:
                try:
                    y_exp .append(limits [v2]['exp' ]) 
                    y_ep1s.append(limits [v2]['ep1s']) 
                    y_ep2s.append(limits [v2]['ep2s']) 
                    y_em1s.append(limits [v2]['em1s']) 
                    y_em2s.append(limits [v2]['em2s']) 
                    b_V2  .append(limits [v2]['V2']) 
                    # if m == 5: set_trace()
                except: set_trace()

        if len(b_V2) == 0: 
            print('combine failed processing this channel, continue doing to next one')
            continue

        x_err = np.zeros(len(b_V2))
        b_V2.sort(reverse=False)

        for i in range(len(y_exp)):
            y_ep1s[i] = abs(y_ep1s[i] - y_exp[i]) 
            y_ep2s[i] = abs(y_ep2s[i] - y_exp[i]) 
            y_em1s[i] = abs(y_em1s[i] - y_exp[i]) 
            y_em2s[i] = abs(y_em2s[i] - y_exp[i]) 
            

        # if Mass == '5' and V == '0.00145602197786': set_trace()
       
        exp = rt.TGraph           (len(b_V2), np.array(b_V2), np.array(y_exp))
        gr1 = rt.TGraphAsymmErrors(len(b_V2), np.array(b_V2), np.array(y_exp), np.array(x_err), np.array(x_err), np.array(y_em1s), np.array(y_ep1s))
        gr2 = rt.TGraphAsymmErrors(len(b_V2), np.array(b_V2), np.array(y_exp), np.array(x_err), np.array(x_err), np.array(y_em2s), np.array(y_ep2s))
        
        rt.gStyle.SetOptStat(0000)
        # B_V2 = np.logspace(-11, -1, 10, base=10)
        # B_Y  = np.logspace(-4, 4, 10, base=10)
        B_V2 = np.logspace(-11, 1, 120, base=10)
        B_Y  = np.logspace(-4, 9, 150, base=10)
        r1g = rt.TGraph           (len(B_V2), np.array(B_V2), np.ones(len(B_V2)))
        r1g.SetLineColor(rt.kRed+1); r1g.SetLineWidth(1)
        framer = rt.TH2F('framer', 'framer', len(B_V2)-1, B_V2, len(B_Y)-1, B_Y)
        # framer.GetYaxis().SetRangeUser(0.0001,10000)
        # framer.GetXaxis().SetRangeUser(0.00000000001, 0.1)
        framer.GetYaxis().SetRangeUser(0.0001,1000000000)
        framer.GetXaxis().SetRangeUser(0.00000000001, 10.)

        if ch == 'mmm': 
            framer.SetTitle('m_{N} = %d GeV,  #mu#mu#mu; |V_{#mu N}|^{2}; r' %mass)
        if ch == 'eee':
            framer.SetTitle('m_{N} = %d GeV,  eee; |V_{e N}|^{2}; r' %mass)
        if ch == 'mem_OS':
            framer.SetTitle('m_{N} = %d GeV,  #mu#mue OS; |V_{#mu N}|^{2}; r' %mass)
        if ch == 'mem_SS':
            framer.SetTitle('m_{N} = %d GeV,  #mu#mue SS; |V_{#mu N}|^{2}; r' %mass)
        if ch == 'eem_OS':
            framer.SetTitle('m_{N} = %d GeV,  ee#mu OS; |V_{e N}|^{2}; r' %mass)
        if ch == 'eem_SS':
            framer.SetTitle('m_{N} = %d GeV,  ee#mu SS; |V_{e N}|^{2}; r' %mass)

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
        can.cd(); can.SetLogy(); can.SetLogx()
        # can.SetBottomMargin(0.15)
        framer.Draw()
        # can.Update()
        gr2.Draw('same, E1')
        gr2.Draw('same, E3')
        # can.Update()
        gr1.Draw('same, E1')
        gr1.Draw('same, E3')
        # can.Update()
        exp.Draw('same, LP')
        # can.Update()
        r1g.Draw('same')
        # can.Update()

        leg = rt.TLegend(.4,.75,.8,.88)
        leg.AddEntry(exp, 'Expected', 'LP')
        leg.AddEntry(gr1, 'Expected #pm 1 #sigma', 'E3')
        leg.AddEntry(gr2, 'Expected #pm 2 #sigma', 'E3')
        leg.Draw('apez same')

        
        # plotfactory.showlogopreliminary()
        plotfactory.showlumi('N#rightarrow%s; mass = %d GeV'%(ch,mass))
        can.Update()
        
        #calculate and plot the intersection
        # if mass != 5: continue
        intersection_exp_x, intersection_exp_y = intersection(np.array(b_V2), np.array(y_exp ), np.array(b_V2), np.ones(len(b_V2)))
        intersection_ep1_x, intersection_ep1_y = intersection(np.array(b_V2), np.array(y_exp) + np.array(y_ep1s), np.array(b_V2), np.ones(len(b_V2)))
        intersection_ep2_x, intersection_ep2_y = intersection(np.array(b_V2), np.array(y_exp) + np.array(y_ep2s), np.array(b_V2), np.ones(len(b_V2)))
        intersection_em1_x, intersection_em1_y = intersection(np.array(b_V2), np.array(y_exp) - np.array(y_em1s), np.array(b_V2), np.ones(len(b_V2)))
        intersection_em2_x, intersection_em2_y = intersection(np.array(b_V2), np.array(y_exp) - np.array(y_em2s), np.array(b_V2), np.ones(len(b_V2)))

        containsEmptyArrays = False
        for intersections in [intersection_exp_x,intersection_ep1_x,intersection_ep2_x,intersection_em1_x,intersection_em2_x]:
            if len(intersections) == 0: 
                containsEmptyArrays = True
                continue
        
        if containsEmptyArrays: continue
        if mass == 5: continue

        intersection_exp = rt.TGraph(len(intersection_exp_x), np.array(intersection_exp_x), np.array(intersection_exp_y))
        intersection_ep1 = rt.TGraph(len(intersection_ep1_x), np.array(intersection_ep1_x), np.array(intersection_ep1_y))
        intersection_ep2 = rt.TGraph(len(intersection_ep2_x), np.array(intersection_ep2_x), np.array(intersection_ep2_y))
        intersection_em1 = rt.TGraph(len(intersection_em1_x), np.array(intersection_em1_x), np.array(intersection_em1_y))
        intersection_em2 = rt.TGraph(len(intersection_em2_x), np.array(intersection_em2_x), np.array(intersection_em2_y))

        intersection_exp.SetMarkerColor(rt.kRed+2)
        intersection_ep1.SetMarkerColor(rt.kGreen+2)
        intersection_ep2.SetMarkerColor(rt.kOrange)
        intersection_em1.SetMarkerColor(rt.kGreen+2)
        intersection_em2.SetMarkerColor(rt.kOrange)

        for intersectionPoints in [intersection_exp,intersection_ep1,intersection_ep2,intersection_em1,intersection_em2]:
            intersectionPoints.SetMarkerStyle(29)
            intersectionPoints.SetMarkerSize(2)
            intersectionPoints.Draw('same, P')

        minNumberOfIntersections = 10
        for intersections in [intersection_exp_x, intersection_ep1_x, intersection_ep2_x, intersection_em1_x, intersection_em2_x]:
            if len(intersections) < minNumberOfIntersections: 
                minNumberOfIntersections = len(intersections) 
        
        for i in range(2):
            try:
                if i == 0: 
                    index = 0
                    ExclusionLimits2D_low['masses'].append(float(mass))
                    ExclusionLimits2D_low['x_err'] .append(0.)
                    ExclusionLimits2D_low['y_exp'] .append(float(min(intersection_exp_x)))
                    ExclusionLimits2D_low['y_ep1s'].append(abs(float(min(intersection_ep1_x))-float(min(intersection_exp_x))))
                    ExclusionLimits2D_low['y_ep2s'].append(abs(float(min(intersection_ep2_x))-float(min(intersection_exp_x))))
                    ExclusionLimits2D_low['y_em1s'].append(abs(float(min(intersection_exp_x))-float(min(intersection_em1_x))))
                    ExclusionLimits2D_low['y_em2s'].append(abs(float(min(intersection_exp_x))-float(min(intersection_em2_x))))
                if (i == 1) and (minNumberOfIntersections > 1): 
                    index = -1
                    ExclusionLimits2D_high['masses'].append(float(mass))
                    ExclusionLimits2D_high['x_err'] .append(0.)
                    ExclusionLimits2D_high['y_exp'] .append(float(max(intersection_exp_x)))
                    ExclusionLimits2D_high['y_ep1s'].append(abs(float(max(intersection_em1_x))-float(max(intersection_exp_x))))
                    ExclusionLimits2D_high['y_ep2s'].append(abs(float(max(intersection_em2_x))-float(max(intersection_exp_x))))
                    ExclusionLimits2D_high['y_em1s'].append(abs(float(max(intersection_exp_x))-float(max(intersection_ep1_x))))
                    ExclusionLimits2D_high['y_em2s'].append(abs(float(max(intersection_exp_x))-float(max(intersection_ep2_x))))
            except: 
                print('exception!!!!!!')
                set_trace()

        # if mass == 8: set_trace()
        if not os.path.isdir(output_dir + 'pdf'): os.mkdir(output_dir + 'pdf')
        if not os.path.isdir(output_dir + 'png'): os.mkdir(output_dir + 'png')
        if not os.path.isdir(output_dir + 'root'): os.mkdir(output_dir + 'root')

        can.SaveAs(output_dir + 'pdf/M%d_%s_root.pdf' %(mass, ch))
        can.SaveAs(output_dir + 'png/M%d_%s_root.png' %(mass, ch))
        can.SaveAs(output_dir + 'root/M%d_%s_root.root' %(mass, ch))
        
        
    return ExclusionLimits2D_low, ExclusionLimits2D_high

if __name__ == '__main__':
    print('starting draw_limits.py...')
    
    plotfactory.setpfstyle()

    channels = []
    channels.append('mmm')
    # channels.append('mem_OS')
    # channels.append('mem_SS')
    # channels.append('eee')
    # channels.append('eem_OS')
    # channels.append('eem_SS')
    # channels.append('mCombined')
    # channels.append('eCombined')

    for channel in channels:
        #2017
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2017/mmm/20191119_limits'

        #2018
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191120_Aachen'%channel
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191121_RiccardoDatacards'%channel
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweightNormalized'%channel
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweightNormalized_fixed'%channel
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweightNormalized_fixed2'%channel
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191128_WideV2'%channel
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191129_NewDispBin'%channel
        # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191129_NewDispBin'%channel
        base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20200123_AN_Feb'%channel
        # base_dir   = '/Users/dehuazhu/SynologyDrive/PhD/7_Writing/1912_AnalysisNote_HNL/AN-19-272/1_Sections/6_Interpretation/figures/Limits/%s/20191129_NewDispBin'%channel
        input_file = base_dir + '/output.txt'

        output_dir = base_dir + '/plots/' 
        if not os.path.isdir(output_dir): os.mkdir(output_dir)

        ExclusionLimits2D_low, ExclusionLimits2D_high = draw_limits(input_file, output_dir, ch = channel)

        # # now making the 2D plot
        # ExclusionLimits2D = {}
        
        # ExclusionLimits2D['masses'] = [1.,2.,3.,4.,5.,6.,8.,10.,20.]
        # ExclusionLimits2D['x_err']  = np.zeros(len(ExclusionLimits2D['masses']))
        # ExclusionLimits2D['y_exp']  = [2e-4  ,2.5e-6,2e-7  ,3e-8,8e-9 ,4e-9,7e-10 ,4e-10,7e-9 ]
        # ExclusionLimits2D['y_ep1s'] = [1e-4  ,3.5e-6,1e-7  ,2e-8,7e-9 ,2e-9,2e-10 ,2e-10,3e-9 ]
        # ExclusionLimits2D['y_ep2s'] = [5e-4  ,5.5e-6,6e-7  ,5e-8,12e-9,5e-9,8e-10 ,6e-10,8e-9] 
        # ExclusionLimits2D['y_em1s'] = [1e-4  ,0.5e-6,1e-7  ,1e-8,3e-9 ,2e-9,3e-10 ,2e-10,4e-9 ]
        # ExclusionLimits2D['y_em2s'] = [1.4e-4,1.1e-6,1.2e-7,2e-8,5e-9 ,3e-9,5e-10 ,3e-10,6e-9 ]

        # draw_limits2D(ExclusionLimits2D_low, ExclusionLimits2D_high, input_file, output_dir, ch=channel, twoD=False, verbose=False)

        draw_limits2DWithPrompt(ExclusionLimits2D_low, ExclusionLimits2D_high, input_file, output_dir, ch=channel, twoD=False, verbose=False)
