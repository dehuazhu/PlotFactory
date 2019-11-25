import re
from modules.PlotConfigs import SampleCfg
from modules.Samples import setSumWeights

from pdb import set_trace

def makeSignalDict(dataMCPlots,channel):
    if ('mmm' in channel) or ('mem' in channel): ch = 'mu'
    if ('eee' in channel) or ('eem' in channel): ch = 'e'

    signalDict = {}

    for i in ['1','2','3','4','5','6','7','8','9','10','20']:
        signalDict[i] = {}
	signalDict[i]	
	# V0p000547722557505
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
	signalDict['%s'%mass]['V%s'%v]		  = {}
	signalDict['%s'%mass]['V%s'%v]['mass']   = mass
	signalDict['%s'%mass]['V%s'%v]['v']   	  = v
	signalDict['%s'%mass]['V%s'%v]['count']  = hist.obj.GetEntries()
	signalDict['%s'%mass]['V%s'%v]['name']   = 'HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(mass,v,ch) 
    return signalDict

def makeCfgs(signalDict,channel,dataset,ana_dir):
    if ('mmm' in channel) or ('mem' in channel): ch = 'mu'
    if ('eee' in channel) or ('eem' in channel): ch = 'e'
    samples = []
    Vs = [\
        '0p00001', # v2 = 1em10
        '0p000022360679774997898', # v2 = 5em10
        '0p000031622776601683795', # v2 = 1em09 
        '0p00007071067811865475', # v2 = 5em09
        '0p0001', # v2 = 1em08
        '0p00022360679774997898', # v2 = 5em08
        '0p00031622776601683794', # v2 = 1em07
        '0p0007071067811865475', # v2 = 5em07
        '0p001', # v2 = 1em06
        '0p00223606797749979', # v2 = 5em06
        '0p0024494897427831783', # v2 = 6em06
        '0p00282842712474619', # v2 = 8em06
        '0p0031622776601683794', # v2 = 1em05
        '0p00447213595499958', # v2 = 2em05
        '0p005477225575051661', # v2 = 3em05
        '0p006324555320336759', # v2 = 4em05
        '0p007071067811865475', # v2 = 5em05
        '0p008366600265340755', # v2 = 7em05
        # '0p01', # v2 = 0.0001
        # '0p01414213562373095', # v2 = 0.0002 
        # '0p015811388300841896', # v2 = 0.00025
        # '0p017320508075688773', # v2 = 0.0003
        # '0p022360679774997897', # v2 = 0.0005
        # '0p034641016151377546', # v2 = 0.0012
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
	    name = 'HN3L_M_%s_V_%s_%s_massiveAndCKM_LO'%(mass,newV,ch) 
            sample = makeSample(name,subdir=subdir,dataset=dataset,channel=channel,analysis_dir=ana_dir) 
            samples.append(sample)
    samples=setSumWeights(samples)

    return samples

def makeSample(name,subdir,dataset='2018',channel='mmm',server='starseeker',analysis_dir=''):
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
                sig_dir = analysis_dir + 'production_20191027_Signal_mmm/'

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
                sig_dir = analysis_dir + 'production_20191105_Signal_mem'
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
                sig_dir = analysis_dir + 'production_20191105_Signal_eee'
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
                sig_dir = analysis_dir + 'production_20191105_Signal_eem'
                DY_dir = analysis_dir + bkg_dir
            dataA_name = 'Single_ele_2018A'; dataB_name = 'Single_ele_2018B'; dataC_name = 'Single_ele_2018C'; dataD_name = 'Single_ele_2018D';
            
    sample = SampleCfg(name=name, dir_name=subdir, ana_dir=sig_dir, tree_prod_name='HNLTreeProducer', is_signal = True, is_reweightSignal = True)
    return sample


def reweightSignals(inputPlots, useMultiprocess, ana_dir, hist_cfg, channel):
    print('#########################')
    print('# reweighting signals')
    print('#########################')
    dataset = '2018'

    for inputPlotKey in inputPlots:
        currentDataMCPlot = inputPlots[inputPlotKey]

        # generate a dictinary with existing signals
        signalDict = makeSignalDict(currentDataMCPlot,channel)

        # make a cfg list for producing the missing signal histograms
	samples = makeCfgs(signalDict,channel,dataset,ana_dir)

    return samples
