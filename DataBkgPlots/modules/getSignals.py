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
from socket import gethostname

def getSignals(verbose=False):
    '''
    ###################################
    ## preparing a signal dictionary ##
    ###################################
    '''
    # read input
    with open('modules/signals2.py', 'r') as f_in:
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

        originalLine = line
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
        # v    = re.sub('p', '.', v)
        # v    = re.sub('M.V', '', v)
        v    = re.sub('.*V', '', v)
        Mass, V = mass, v


        # try: signals['M' + Mass + '_V' + V + '_' + mode]['mass'] = float(mass)
        # except:
            # signals['M' + Mass + '_V' + V + '_' + mode] = OrderedDict()
            # signals['M' + Mass + '_V' + V + '_' + mode]['mass'] = float(mass)

        try:
            signals['HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(Mass,v,mode)]['mass']= OrderedDict() 
        except:
            signals['HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(Mass,v,mode)] = OrderedDict() 
            signals['HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(Mass,v,mode)]['mass'] = float(mass) 


        # V2 = None
        if 'v2=' in line: 
            V2 = None
            V2 = re.sub('.*v2=', '', line) 
            signals['HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(Mass,v,mode)]['V2'] = float(V2) 
            if verbose: print (V2, float(V)**2)

        # xsec = None
        if 'xs=' in line: 
            xsec = None
            xsec = re.sub('.*xs=', '', line) 
            signals['HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(Mass,v,mode)]['xsec'] = float(xsec) 

        # xsec_err = None
        if 'xse=' in line: 
            xsec_err = None
            xsec_err = re.sub('.*xse=', '', line) 
            signals['HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(Mass,v,mode)]['xsec_err'] = float(xsec_err) 

    if verbose:
        for k in signals.keys(): 
            for kk in signals[k].keys():
                print (k, kk, signals[k][kk])
            print ('\n')
    
    return signals

