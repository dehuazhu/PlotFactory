'''
#########################################################################
## FIRST SOURCE THE COMPATIBLE ROOT VERSION:                           ##
## (FOR RUNNING THE DIFFERENT SCRIPTS ALWAYS START A NEW BASH SESSION) ##
## cd /t3home/vstampf/CMSSW_9_4_6_patch1/src/; cmsenv; cd -            ##
## IN ORDER TO RUN THIS CODE EXECUTE:  DC = dataCards(CH)              ##
## WHERE CH = 'mmm', eem_OS', ...                                      ##
## THEN EXCUTE DC.make_inputs() TO GENERATE THE DC                     ##
#########################################################################
'''
import ROOT as rt
from collections import OrderedDict
from re import sub
from pdb import set_trace
from copy import deepcopy
from glob import glob
from os import system
import os



class dataCards(object):

    def __init__(self, channel, in_folders, out_folder):
        # self.ch = ch
        # self.out_folder = '/t3home/vstampf/eos/plots/limits/inputs/data_cards_aug_20/'
        # self.in_folders = glob('/work/dezhu/3_figures/1_DataMC/FinalStates/0_datacards_v2_NewBinning/*%s_disp*/root/linear/' %self.ch)
        self.ch = channel
        self.in_folders = in_folders
        self.out_folder = out_folder
    

    def printDataCards(self, signal_name):
        '''
            #############################
            ## writes the DC for       ##
            ## combine for all signals ##
            #############################
        '''

        with open(self.out_folder + 'hnl_%s_dc_%s.txt' %(signal_name, self.ch), 'w') as f:

            if self.verbose: print (self.out_folder+ 'hnl_%s_dc_%s.txt' %(signal_name, self.ch))

            disp_bins = self.disp_bins
            ch = self.ch

            rate_obs_d1,  rate_obs_d2,  rate_obs_d3  = self.rates[disp_bins[0]]['obs' ].Integral(), self.rates[disp_bins[1]]['obs' ].Integral(), self.rates[disp_bins[2]]['obs' ].Integral()
            rate_conv_d1, rate_conv_d2, rate_conv_d3 = self.rates[disp_bins[0]]['conv'].Integral(), self.rates[disp_bins[1]]['conv'].Integral(), self.rates[disp_bins[2]]['conv'].Integral()
            rate_fake_d1, rate_fake_d2, rate_fake_d3 = self.rates[disp_bins[0]]['fake'].Integral(), self.rates[disp_bins[1]]['fake'].Integral(), self.rates[disp_bins[2]]['fake'].Integral()
            rate_sig_d1,  rate_sig_d2,  rate_sig_d3  = self.rates[disp_bins[0]][signal_name ].Integral(), self.rates[disp_bins[1]][signal_name ].Integral(), self.rates[disp_bins[2]][signal_name ].Integral()
    
            # to prevent a zero denominator, rate_fake* should never be a complete zero
            if rate_fake_d1 < 0.01: rate_fake_d1 = 0.01
            if rate_fake_d2 < 0.01: rate_fake_d2 = 0.01
            if rate_fake_d2 < 0.01: rate_fake_d2 = 0.01

            if self.vv: rate_vv_d1,   rate_vv_d2,   rate_vv_d3  = self.rates[disp_bins[0]]['vv' ].Integral(), self.rates[disp_bins[2]]['vv' ].Integral(), self.rates[disp_bins[2]]['vv' ].Integral()

            name_tab = '\t'; xs_tab = '\t'
            if len(signal_name) < len('M2_Vp00244948974278'):   name_tab = '\t\t'
            if len(signal_name) < len('M2_Vp00244948974278')-2:
                name_tab = '\t\t\t\t'
                xs_tab   = name_tab

            n_samples = 3
            if not self.vv: n_samples = 2 

            print('max     3     number of categories', file=f)
            print('jmax    %s     number of samples minus one' %n_samples,file=f)
            print('kmax    *     number of nuisance parameters',file=f)
            print('---------------------------------------------------------',file=f)
            print('shapes *             %s   hnl_mll_combine_input_%s.root %s/$PROCESS %s/$PROCESS_$SYSTEMATIC' %(disp_bins[0], ch, disp_bins[0], disp_bins[0]),file=f  )
            print('shapes *             %s   hnl_mll_combine_input_%s.root %s/$PROCESS %s/$PROCESS_$SYSTEMATIC' %(disp_bins[1], ch, disp_bins[1], disp_bins[1]),file=f  )
            print('shapes *             %s   hnl_mll_combine_input_%s.root %s/$PROCESS %s/$PROCESS_$SYSTEMATIC' %(disp_bins[2], ch, disp_bins[2], disp_bins[2]),file=f  )
            print('---------------------------------------------------------',file=f)
            print('bin                  %s\t\t\t %s\t\t\t %s\t\t\t' %(disp_bins[0], disp_bins[1], disp_bins[2]),file=f)
            print('observation          %.2f \t\t\t%.2f \t\t\t     %.2f '%(rate_obs_d1, rate_obs_d2, rate_obs_d3),file=f)
            print('-----------------------------------------------------------------',file=f)
            if self.vv:
                print ('bin                              %s\t\t\t %s\t\t\t %s\t\t\t %s\t\t\t '\
                                                       '%s\t\t\t %s\t\t\t %s\t\t\t %s\t\t\t '\
                                                       '%s\t\t\t %s\t\t\t %s\t\t\t %s\t\t\t' %(disp_bins[0], disp_bins[0], disp_bins[0], disp_bins[0], disp_bins[1], disp_bins[1], disp_bins[1], disp_bins[1], 
                                                                                               disp_bins[2], disp_bins[2], disp_bins[2], disp_bins[2]),file=f)
                print ('process                          0                       1                       2                       3                       '\
                                                       '0                       1                       2                       3                       '\
                                                       '0                       1                       2                       3                       ',file=f)
                print ('process                          %s%s conversions            nonprompt              VV                      '\
                                                       '%s%s conversions             nonprompt              VV                      '\
                                                       '%s%s conversions             nonprompt              VV' %(signal_name, name_tab, signal_name, name_tab, signal_name, name_tab),file=f)
                print ('rate                             %.2f\t\t\t\t\t %.2f\t\t\t\t\t %.2f\t\t\t\t\t  %.2f\t\t\t\t\t '\
                                                       '%.2f\t\t\t\t\t %.2f\t\t\t\t\t %.2f\t\t\t\t\t  %.2f\t\t\t\t\t '\
                                                       '%.2f\t\t\t\t\t %.2f\t\t\t\t\t %.2f\t\t\t\t\t %.2f' %(rate_sig_d1, rate_conv_d1, rate_fake_d1, rate_vv_d1, 
                                                                                                             rate_sig_d2, rate_conv_d2, rate_fake_d2, rate_vv_d2, rate_sig_d3, rate_conv_d3, rate_fake_d3, rate_vv_d3),file=f)
                print ('-------------------------------------------------------------------------------------------------------------------',file=f)
                print ('lumi                     lnN     1.026                   1.026                   -                       1.026                   '\
                                                       '1.026                   1.026                   -                       1.026                   '\
                                                       '1.026                   1.026                   -                       1.026                   ',file=f)
                print ('norm_conv                lnN     -                       1.1                     -                       -                       '\
                                                       '-                       1.1                     -                       -                       '\
                                                       '-                       1.1                     -                       -                       ',file=f)
                print ('norm_vv                  lnN     -                       -                       -                       1.1                     '\
                                                       '-                       -                       -                       1.1                     '\
                                                       '-                       -                       -                       1.1                     ',file=f)
                print ('norm_fr_d1               lnN     -                       -                       1.2                     -                       '\
                                                       '-                       -                       -                       -                       '\
                                                       '-                       -                       -                       -                       ',file=f)
                print ('norm_fr_d2               lnN     -                       -                       -                       -                       '\
                                                       '-                       -                       1.2                     -                       '\
                                                       '-                       -                       -                       -                       ',file=f)
                print ('norm_fr_d3               lnN     -                       -                       -                       -                       '\
                                                       '-                       -                       -                       -                       '\
                                                       '-                       -                       1.2                     -                       ',file=f)
                print ('norm_sig                 lnN     1.2                     -                       -                       -                       '\
                                                       '1.2                     -                       -                       -                       '\
                                                       '1.2                     -                       -                       -                       ',file=f)
            if not self.vv:
                print ('bin                              %s\t\t\t %s\t\t\t %s\t\t\t '\
                                                       '%s\t\t\t %s\t\t\t %s\t\t\t '\
                                                       '%s\t\t\t %s\t\t\t %s\t\t\t' %(disp_bins[0], disp_bins[0], disp_bins[0], disp_bins[1], disp_bins[1], disp_bins[1], disp_bins[2], disp_bins[2], disp_bins[2]),file=f)
                print ('process                          0                       1                       2                       '\
                                                       '0                       1                       2                       '\
                                                       '0                       1                       2       ',file=f)
                print ('process                          %s%s conversions             nonprompt              '\
                                                       '%s%s conversions             nonprompt              '\
                                                       '%s%s conversions             nonprompt' %(signal_name, name_tab, signal_name, name_tab, signal_name, name_tab),file=f)
                print ('rate                             %.2f\t\t\t\t\t %.2f\t\t\t\t\t %.2f\t\t\t\t\t '\
                                                       '%.2f\t\t\t\t\t %.2f\t\t\t\t\t %.2f\t\t\t\t\t '\
                                                       '%.2f\t\t\t\t\t %.2f\t\t\t\t\t %.2f' %(rate_sig_d1, rate_conv_d1, rate_fake_d1, rate_sig_d2, rate_conv_d2, rate_fake_d2, rate_sig_d3, rate_conv_d3, rate_fake_d3),file=f)
                print ('-------------------------------------------------------------------------------------------------------------------',file=f)
                print ('lumi                     lnN     1.026                   1.026                   -                       '\
                                                       '1.026                   1.026                   -                       '\
                                                       '1.026                   1.026                   -                       ',file=f)
                print ('norm_conv                lnN     -                       1.1                     -                       '\
                                                       '-                       1.1                     -                       '\
                                                       '-                       1.1                     -                       ',file=f)
                print ('norm_fr_d1               lnN     -                       -                       1.2                     '\
                                                       '-                       -                       -                       '\
                                                       '-                       -                       -                       ',file=f)
                print ('norm_fr_d2               lnN     -                       -                       -                       '\
                                                       '-                       -                       1.2                     '\
                                                       '-                       -                       -                       ',file=f)
                print ('norm_fr_d3               lnN     -                       -                       -                       '\
                                                       '-                       -                       -                       '\
                                                       '-                       -                       1.2                     ',file=f)
                print ('norm_sig                 lnN     1.2                     -                       -                       '\
                                                             '1.2                     -                       -                       '\
                                                             '1.2                     -                       -                       ',file=f)
            print ('disp1 autoMCStats 0 0 1',file=f)
            print ('disp2 autoMCStats 0 0 1',file=f)
            print ('disp3 autoMCStats 0 0 1',file=f)
     
        f.close()

    def make_inputs(self, verbose=False, has_signals=True):
        '''
            ###########################################
            ## reads inputs from the hnl_m_12 stack  ##
            ## and creates the DC + input root files ##
            ###########################################
        '''
        self.vv = False
        self.verbose = verbose

        rates = OrderedDict()

        fout = rt.TFile.Open(self.out_folder + 'hnl_mll_combine_input_%s.root' %self.ch, 'recreate')

        self.disp_bins = []

        # #2017
        # for in_folder in self.in_folders:
            # disp_bin = sub('.*disp', 'disp', sub('/root.*','', in_folder))
            # fin = rt.TFile(in_folder + 'hnl_m_12_money.root')

        #2018
        in_folder = self.in_folders[0]
        for disp_bin in ['disp1','disp2','disp3']:
            fin_name = ''
            for fileName in os.listdir(in_folder): 
                if disp_bin in fileName: fin_name = fileName
            if fin_name == '': set_trace()
            fin = rt.TFile(in_folder + fin_name)
        # end 2017/2018 difference

            self.disp_bins.append(disp_bin)
            if verbose: print (disp_bin)

            can = fin.Get('can')
            pad = can.GetPrimitive('can_1')

            h_list = pad.GetListOfPrimitives()

            h_dict = OrderedDict()

            # set_trace()
            # for h in h_list[:len(h_list)/2+1]:
                # h_name = h.GetName()
                # if 'HN3L' in h_name: 
                    # h_name = sub('.*HN3L_M_', 'M', h_name)
                    # h_name = sub('_V_0', '_V', h_name)
                    # h_name = sub('_mu_massiveAndCKM_LO', '', h_name)
                    # h_name = sub('_e_massiveAndCKM_LO', '', h_name)
                    # h.SetName(h_name)
                    # h_dict[h_name] = h
                # elif 'data' in h_name: 
                    # h.SetName('data_obs')
                    # h_dict['data_obs'] = h

            for h in h_list:
                h_name = h.GetName()
                if ('TFrame' in h_name) or ('TPave' in h_name): continue
                elif 'Dirac' in h_name: continue  
                elif 'HN3L' in h_name: 
                    # if 'datacard_v2_SigReweight_d471bd1f9ff31e2b2834b49a955c980a_HN3L_M_6_V_0p00202484567313_mu_massiveAndCKM_LO_hnl_m_12_money_disp1_0p5_fine_HN3L_M_6_V_0p00202484567313_mu_massiveAndCKM_' in h_name: set_trace()
                    name = sub('_hnl_m_12_money_disp.*', '', h_name)
                    name = sub('.*HN3L_M_', 'M', name)
                    name = sub('_V_0', '_V', name)
                    name = sub('_mu_massiveAndCKM_LO', '', name)
                    name = sub('_e_massiveAndCKM_LO', '', name)
                    h.SetName(name)
                    h_dict[name] = h
                elif 'stack' in h_name:
                    stack = pad.GetPrimitive(h_name)
                else: 
                    # set_trace()
                    continue
                # elif 'data' in h_name: 
                    # h.SetName('data_obs')
                    # h_dict['data_obs'] = h

            for h in stack.GetHists():
                h_name = h.GetName()
                if 'Conversions_DY' in h_name: h_name = 'conversions' #
                if 'WW'             in h_name: h_name = 'VV'
                if 'nonprompt'      in h_name: h_name = 'nonprompt'
                h.SetName(h_name)
                h.SetLineColor(rt.kBlue+2)
                h.SetMarkerColor(rt.kBlue+2)
                # fail-save for negative integrals of prompt bkg
                #TODO this should be fixed in the plotting tool at some point?
                if h.Integral() < 0: 
                    h.Scale(0.001/h.Integral())
                    print ('WARNING: negative integral for conv in', disp_bin)
                
                h_dict[h_name] = h

            if not has_signals: 
                h_dict['dummy_sig'] = h_dict['conversions']
                h_dict['dummy_sig'].SetName('dummy_sig')
                # h_dict['dummy_sig'].Scale(0.01/h_dict['dummy_sig'].Integral())

            # clone prompt bkg to data for blind limits
            # if not h_dict.has_key('data_obs'):
            if 'data_obs' not in h_dict:
                # h_dict['data_obs'] = dc(h_dict['conversions'])
                h_dict['data_obs'] = deepcopy(h_dict['conversions'])
                h_dict['data_obs'].SetName('data_obs')

            # make root file with combine-readable structure
            fout.cd()
            rt.gDirectory.mkdir('%s' %disp_bin)
            fout.cd('%s' %disp_bin)

            for hist in h_dict.keys():
                if verbose: print ('writing', hist)
                h_dict[hist].Write()

            if has_signals:     signals = [sig for sig in h_dict if 'Vp' in sig]
            if not has_signals:  signals = ['dummy_sig']


            rates[disp_bin] = OrderedDict()

            signals = [sig for sig in h_dict if 'Vp' in sig]
            for s in signals:
                rates[disp_bin][s]   = h_dict[s]
            rates[disp_bin]['conv']  = h_dict['conversions']
            rates[disp_bin]['fake']  = h_dict['nonprompt' ]
            rates[disp_bin]['obs' ]  = h_dict['data_obs'   ]
            if 'VV' in h_dict: self.vv = True
            # if h_dict.has_key('VV'): self.vv = True
       
        signals = [sig for sig in rates[disp_bin] if 'Vp' in sig]
        self.rates = rates
        for signal in signals:
            self.printDataCards(signal)

        fout.Close()
        print('datacards generated to %s'%self.out_folder)

if __name__ == '__main__':
    channels = []
    channels.append('mmm')
    channels.append('mem_OS')
    channels.append('mem_SS')
    channels.append('eee')
    channels.append('eem_OS')
    channels.append('eem_SS')

    for channel in channels:
        #original 2017
        # in_folders = glob('/work/dezhu/3_figures/1_DataMC/FinalStates/0_datacards_v2_NewBinning/*%s_disp*/root/linear/' %channel)
        # out_base = '/work/dezhu/3_figures/2_Limits/2017/mmm/20191119_limits'
        
        #new 2018
        # in_folders = glob('/work/dezhu/3_figures/1_DataMC/FinalStates/2018/0_datacards_v1/%s/root/linear/' %channel)
        # in_folders = glob('/work/dezhu/3_figures/1_DataMC/FinalStates/2018/0_datacards_v2_SignalReweight/%s/root/linear/' %channel)
        # in_folders = glob('/work/dezhu/3_figures/1_DataMC/FinalStates/2018/0_datacards_v3_SignalReweightNormalized/%s/root/linear/' %channel)
        # in_folders = glob('/work/dezhu/3_figures/1_DataMC/FinalStates/2018/%s/datacard_v3_SigReweightNormalized_fixed/root/linear/' %channel)
        # in_folders = glob('/work/dezhu/3_figures/1_DataMC/FinalStates/2018/%s/datacard_v3_SigReweightNormalized_fixed2/root/linear/' %channel)
        in_folders = glob('/work/dezhu/3_figures/1_DataMC/FinalStates/2018/%s/datacard_v5_BetterDisplacementBin/root/linear/' %channel)

        # output_base = '/work/dezhu/3_figures/2_Limits/2018/%s/20191120_Aachen'%channel
        # output_base = '/work/dezhu/3_figures/2_Limits/2018/%s/20191125_SignalReweight'%(channel)
        output_base = '/work/dezhu/3_figures/2_Limits/2018/%s/20191129_NewDispBin'%(channel)
        
        output_folder = output_base + '/datacards/'

        if not os.path.isdir(output_base): os.mkdir(output_base)
        if not os.path.isdir(output_folder): os.mkdir(output_folder)

        DC = dataCards(channel, in_folders, output_folder)
        DC.make_inputs(verbose=False)
        
