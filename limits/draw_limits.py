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
from termcolor import colored
import plotfactory    
from socket import gethostname


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

        if ((ch == 'mmm') or (ch == 'mem_OS') or (ch == 'mem_SS')): mode = 'mu'
        if ((ch == 'eee') or (ch == 'eem_OS') or (ch == 'eem_SS')): mode = 'e'

        if '_e_' in line:   mode = 'e'  
        if '_mu_' in line:  mode = 'mu' 
        if '_tau_' in line: mode = 'tau'

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
    set_trace()

    b     = np.arange(0., 11, 1)
    req1  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    ixs = OrderedDict()

    #sort the dictionary after v values
    limits = OrderedDict(sorted(limits.items(),key=lambda t: t[1]['V']))

    for m in masses:
        print(colored('doing MASS = %d GeV'%m,'green'))

        y_exp = []; y_ep1s = []; y_ep2s = []; y_em2s = []; y_em1s = [];  
        v2s   = [lim for lim in limits if 'M%d_' %m in lim]
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
        B_V2 = np.logspace(-11, -1, 10, base=10)
        B_Y  = np.logspace(-4, 4, 10, base=10)
        r1g = rt.TGraph           (len(B_V2), np.array(B_V2), np.ones(len(B_V2)))
        r1g.SetLineColor(rt.kRed+1); r1g.SetLineWidth(1)
        framer = rt.TH2F('framer', 'framer', len(B_V2)-1, B_V2, len(B_Y)-1, B_Y)
        framer.GetYaxis().SetRangeUser(0.0001,10000)
        framer.GetXaxis().SetRangeUser(0.00000000001, 0.1)

        if ch == 'mmm': 
            framer.SetTitle('m_{N} = %d GeV,  #mu#mu#mu; |V_{#mu N}|^{2}; r' %m)
        if ch == 'eee':
            framer.SetTitle('m_{N} = %d GeV,  eee; |V_{e N}|^{2}; r' %m)
        if ch == 'mem_OS':
            framer.SetTitle('m_{N} = %d GeV,  #mu#mue OS; |V_{#mu N}|^{2}; r' %m)
        if ch == 'mem_SS':
            framer.SetTitle('m_{N} = %d GeV,  #mu#mue SS; |V_{#mu N}|^{2}; r' %m)
        if ch == 'eem_OS':
            framer.SetTitle('m_{N} = %d GeV,  ee#mu OS; |V_{e N}|^{2}; r' %m)
        if ch == 'eem_SS':
            framer.SetTitle('m_{N} = %d GeV,  ee#mu SS; |V_{e N}|^{2}; r' %m)

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
        can.Update()
        gr2.Draw('same, E1')
        gr2.Draw('same, E3')
        can.Update()
        gr1.Draw('same, E1')
        gr1.Draw('same, E3')
        can.Update()
        exp.Draw('same, LP')
        can.Update()
        r1g.Draw('same')
        can.Update()

        leg = rt.TLegend(.4,.75,.8,.88)
        leg.AddEntry(exp, 'Expected', 'LP')
        leg.AddEntry(gr1, 'Expected #pm 1 #sigma', 'E3')
        leg.AddEntry(gr2, 'Expected #pm 2 #sigma', 'E3')
        leg.Draw('apez same')

        
        # plotfactory.showlogopreliminary()
        plotfactory.showlumi('N#rightarrow%s; mass = %d GeV'%(ch,m))
        can.Update()

        if not os.path.isdir(output_dir + 'pdf'): os.mkdir(output_dir + 'pdf')
        if not os.path.isdir(output_dir + 'png'): os.mkdir(output_dir + 'png')
        if not os.path.isdir(output_dir + 'root'): os.mkdir(output_dir + 'root')

        can.SaveAs(output_dir + 'pdf/M%d_%s_root.pdf' %(m, ch))
        can.SaveAs(output_dir + 'png/M%d_%s_root.png' %(m, ch))
        can.SaveAs(output_dir + 'root/M%d_%s_root.root' %(m, ch))

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
    # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweightNormalized'%channel
    # base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweightNormalized_fixed'%channel
    base_dir   = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweightNormalized_fixed2'%channel
    input_file = base_dir + '/output.txt'

    output_dir = base_dir + '/plots/' 
    if not os.path.isdir(output_dir): os.mkdir(output_dir)

    draw_limits(input_file, output_dir, ch = channel)
