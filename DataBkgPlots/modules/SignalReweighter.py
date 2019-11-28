import re
from modules.PlotConfigs import SampleCfg
from modules.Samples import setSumWeights

from pdb import set_trace
###########################################
from modules.getSignals import getSignals

##########################################
def makeSignalDict(dataMCPlots,channel):
    if ('mmm' in channel) or ('mem' in channel): ch = 'mu'
    if ('eee' in channel) or ('eem' in channel): ch = 'e'

    signalDict = {}

    for i in ['1','2','3','4','5','6','7','8','9','10','11','15','20']:
        signalDict[i] = {}
    for i, hist in enumerate(dataMCPlots.histos):
        name = hist.name
        if 'HN3L' not in name: continue
        if 'Dirac' in name: continue
        mass = re.sub('.*_M_','',name)
        mass = re.sub('_.*','',mass)
        mass = int(mass)
        v    = re.sub('.*_V_','',name)
        v    = re.sub('_.*','',v)
        # v    = re.sub('p','.',v)
        # v2   = float(v)**2
        try:
            signalDict['%s'%mass]['V%s'%v]		  = {}
            signalDict['%s'%mass]['V%s'%v]['mass']   = mass
            signalDict['%s'%mass]['V%s'%v]['v']   	  = v
            signalDict['%s'%mass]['V%s'%v]['count']  = hist.obj.GetEntries()
            signalDict['%s'%mass]['V%s'%v]['name']   = 'HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(mass,v,ch) 
        except: set_trace()
    return signalDict

def makeCfgs(signalDict,channel,dataset,ana_dir,signals):
    if ('mmm' in channel) or ('mem' in channel): ch = 'mu'
    if ('eee' in channel) or ('eem' in channel): ch = 'e'
    samples = []
    Vs = [\
        '0p00001', # v2 = 1em10
        '0p00001414213562', # v2 = 2em10
        '0p00001732050808', # v2 = 3em10
        '0p00002', # v2 = 4em10
        '0p000022360679774997898', # v2 = 5em10
        '0p00002449489743', # v2 = 6em10
        '0p00002645751311', # v2 = 7em10
        '0p00002828427125', # v2 = 8em10
        '0p00003', # v2 = 9em10

        '0p000031622776601683795', # v2 = 1em09 
        '0p00004472135955', # v2 = 2em09
        '0p00005477225575', # v2 = 3em09
        '0p0000632455532', # v2 = 4em09
        '0p00007071067811865475', # v2 = 5em09
        '0p00007745966692', #v2 = 6em09
        '0p00008366600265', #v2 = 7em09
        '0p0000894427191', #v2 = 8em09
        '0p00009486832981', #v2 = 9em09

        '0p0001', # v2 = 1em08
        '0p0001414213562', # v2 = 2em08
        '0p0001732050808', # v2 = 3em08
        '0p0002', # v2 = 4em08
        '0p00022360679774997898', # v2 = 5em08
        '0p0002449489743', # v2 = 6em08
        '0p0002645751311', # v2 = 7em08
        '0p0002828427125', # v2 = 8em08
        '0p0003', # v2 = 9em08

        '0p00031622776601683795', # v2 = 1em07 
        '0p0004472135955', # v2 = 2em07
        '0p0005477225575', # v2 = 3em07
        '0p000632455532', # v2 = 4em07
        '0p0007071067811865475', # v2 = 5em07
        '0p0007745966692', #v2 = 6em07
        '0p0008366600265', #v2 = 7em07
        '0p000894427191', #v2 = 8em07
        '0p0009486832981', #v2 = 9em07

        '0p001', # v2 = 1em06
        '0p001414213562', # v2 = 2em06
        '0p001732050808', # v2 = 3em06
        '0p002', # v2 = 4em06
        '0p0022360679774997898', # v2 = 5em06
        '0p002449489743', # v2 = 6em06
        '0p002645751311', # v2 = 7em06
        '0p002828427125', # v2 = 8em06
        '0p003', # v2 = 9em06

        '0p0031622776601683795', # v2 = 1em05 
        '0p004472135955', # v2 = 2em05
        '0p005477225575', # v2 = 3em05
        '0p00632455532', # v2 = 4em05
        '0p007071067811865475', # v2 = 5em05
        '0p007745966692', #v2 = 6em05
        '0p008366600265', #v2 = 7em05
        '0p00894427191', #v2 = 8em05
        '0p009486832981', #v2 = 9em05

        '0p01', # v2 = 1em04
        '0p01414213562', # v2 = 2em04
        '0p01732050808', # v2 = 3em04
        '0p02', # v2 = 4em04
        '0p022360679774997898', # v2 = 5em04
        '0p02449489743', # v2 = 6em04
        '0p02645751311', # v2 = 7em04
        '0p02828427125', # v2 = 8em04
        '0p03', # v2 = 9em04

        '0p031622776601683795', # v2 = 1em03 
        '0p04472135955', # v2 = 2em03
        '0p05477225575', # v2 = 3em03
        '0p0632455532', # v2 = 4em03
        '0p07071067811865475', # v2 = 5em03
        '0p07745966692', #v2 = 6em03
        '0p08366600265', #v2 = 7em03
        '0p0894427191', #v2 = 8em03
        '0p09486832981', #v2 = 9em03

        '0p1', # v2 = 1em02
        '0p1414213562', # v2 = 2em02
        '0p1732050808', # v2 = 3em02
        '0p2', # v2 = 4em02
        '0p22360679774997898', # v2 = 5em02
        '0p2449489743', # v2 = 6em02
        '0p2645751311', # v2 = 7em02
        '0p2828427125', # v2 = 8em02
        '0p3', # v2 = 9em02

        '0p31622776601683795', # v2 = 1em01 
        '0p4472135955', # v2 = 2em01
        '0p5477225575', # v2 = 3em01
        '0p632455532', # v2 = 4em01
        '0p7071067811865475', # v2 = 5em01
        '0p7745966692', #v2 = 6em01
        '0p8366600265', #v2 = 7em01
        '0p894427191', #v2 = 8em01
        '0p9486832981', #v2 = 9em01
        ]

    for mass in signalDict:
        if signalDict[mass]=={}: continue
        maxEntries = 0
        maxEntriesSampleKey = None
        for v in signalDict[mass]:
            entries = signalDict[mass][v]['count']
            if entries >= maxEntries:
                maxEntries = entries
                maxEntriesSampleKey = v 
        try:
            subdir = signalDict[mass][maxEntriesSampleKey]['name']
        except: set_trace()
        for newV in Vs:
            name = 'HN3L_M_%s_V_%s_%s_massiveAndCKM_LO_reweighted'%(mass,newV,ch) 
            sample = makeSample(name,subdir=subdir,signals=signals,dataset=dataset,channel=channel,analysis_dir=ana_dir) 
            samples.append(sample)
            
    samples=setSumWeights(samples)

    return samples

def makeSample(name,subdir,signals,dataset='2018',channel='mmm',server='starseeker',analysis_dir=''):
    if dataset == '2018':
        if channel == 'mmm':
            if 'lxplus' in server:
                data_dir = analysis_dir+'production_20191027_Data_mmm/'
                bkg_dir = 'production_20191027_Bkg_mmm/'
                sig_dir = analysis_dir + 'production_20191027_Signal_mmm/'
            if 't3' in server:
                data_dir = analysis_dir+'production_20191027_Data_mmm/'
                bkg_dir = 'production_20191027_Bkg_mmm/'
                sig_dir = analysis_dir + 'production_20191027_Signal_mmm/'
            if 'starseeker' in server:
                data_dir = analysis_dir+'production_20191027_Data_mmm/'
                bkg_dir = 'production_20191027_Bkg_mmm/'
                # sig_dir = analysis_dir + 'production_20191027_Signal_mmm/'
                sig_dir = analysis_dir + 'production_20191126_Signal/signals_2018'

            dataA_name = 'Single_mu_2018A'; dataB_name = 'Single_mu_2018B'; dataC_name = 'Single_mu_2018C'; dataD_name = 'Single_mu_2018D';

        if 'mem' in channel:
            if 'lxplus' in server:
                data_dir = '/eos/user/v/vstampf/ntuples/data_2017_m_noskim/'
                bkg_dir = 'bkg_mc_m/'
                sig_dir = 'sig_mc_m/ntuples/'
                DY_dir = analysis_dir + bkg_dir
            if 't3' in server:
                # data_dir = analysis_dir + 'data/'
                # data_dir = 'root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/dezhu/2_ntuples/HN3Lv2.0/mmm/data/'
                data_dir = '/work/dezhu/4_production/vinz'
                bkg_dir = 'vinz/'
                # bkg_dir = 'production_20190306_BkgMC/mmm/ntuples/'
                sig_dir = 'signal/ntuples'
                DY_dir = analysis_dir + bkg_dir
            if 'starseeker' in server:
                data_dir = analysis_dir+'production_20191105_Data_mem'
                bkg_dir = 'production_20191105_Bkg_mem'
                # sig_dir = analysis_dir + 'production_20191105_Signal_mem'
                sig_dir = analysis_dir + 'production_20191126_Signal/signals_2018'
                DY_dir = analysis_dir + bkg_dir
            dataA_name = 'Single_mu_2018A'; dataB_name = 'Single_mu_2018B'; dataC_name = 'Single_mu_2018C'; dataD_name = 'Single_mu_2018D';

        if channel == 'eee':
            if 'lxplus' in server:
                set_trace()
            if 't3' in server:
                set_trace()
            if 'starseeker' in server:
                data_dir = analysis_dir+'production_20191105_Data_eee'
                bkg_dir = 'production_20191105_Bkg_eee'
                # sig_dir = analysis_dir + 'production_20191105_Signal_eee'
                sig_dir = analysis_dir + 'production_20191126_Signal/signals_2018'
                DY_dir = analysis_dir + bkg_dir
            dataA_name = 'Single_ele_2018A'; dataB_name = 'Single_ele_2018B'; dataC_name = 'Single_ele_2018C'; dataD_name = 'Single_ele_2018D';

        if 'eem' in channel:
            if 'lxplus' in server:
                set_trace()
            if 't3' in server:
                set_trace()
            if 'starseeker' in server:
                data_dir = analysis_dir+'production_20191105_Data_eem'
                bkg_dir = 'production_20191105_Bkg_eem'
                # sig_dir = analysis_dir + 'production_20191105_Signal_eem'
                sig_dir = analysis_dir + 'production_20191126_Signal/signals_2018'
                DY_dir = analysis_dir + bkg_dir
            dataA_name = 'Single_ele_2018A'; dataB_name = 'Single_ele_2018B'; dataC_name = 'Single_ele_2018C'; dataD_name = 'Single_ele_2018D';
            
        if (channel in ['mmm','mem_OS','mem_SS']) and ('_mu_' in subdir): 
            if channel == 'mmm': sample = SampleCfg(name=name, dir_name=subdir, ana_dir=sig_dir, tree_prod_name='HNLTreeProducer_mmm', xsec = signals[subdir]['xsec'], is_signal = True, is_reweightSignal = True)
            if 'mem' in channel: sample = SampleCfg(name=name, dir_name=subdir, ana_dir=sig_dir, tree_prod_name='HNLTreeProducer_mem', xsec = signals[subdir]['xsec'], is_signal = True, is_reweightSignal = True)
        if (channel in ['eee','eem_OS','eem_SS']) and ('_e_' in subdir): 
            if channel == 'eee': sample = SampleCfg(name=name, dir_name=subdir, ana_dir=sig_dir, tree_prod_name='HNLTreeProducer_eee', xsec = signals[subdir]['xsec'], is_signal = True, is_reweightSignal = True)
            if 'eem' in channel: sample = SampleCfg(name=name, dir_name=subdir, ana_dir=sig_dir, tree_prod_name='HNLTreeProducer_eem', xsec = signals[subdir]['xsec'], is_signal = True, is_reweightSignal = True)
    # sample = SampleCfg(name=name, dir_name=subdir, ana_dir=sig_dir, xsec = signals[subdir]['xsec'], tree_prod_name='HNLTreeProducer', is_signal = True, is_reweightSignal = True)
    return sample


def reweightSignals(inputPlots, useMultiprocess, ana_dir, hist_cfg, channel):
    print('#########################')
    print('# reweighting signals')
    print('#########################')
    dataset = '2018'

    signals = getSignals()

    for inputPlotKey in inputPlots:
        currentDataMCPlot = inputPlots[inputPlotKey]

        # generate a dictinary with existing signals
        signalDict = makeSignalDict(currentDataMCPlot,channel)

        # make a cfg list for producing the missing signal histograms
        samples = makeCfgs(signalDict,channel,dataset,ana_dir,signals)

    return samples
