import ROOT
import plotfactory
from glob import glob
from pdb import set_trace
import numpy as np

def makechain():
    chain = ROOT.TChain('tree')
    all_files = glob('/mnt/StorageElement1/7_NN/2018/mmm_nonprompt_v8_Endgame/friendtree_fr_nonprompt*')
    for sample in all_files:
        chain.Add(sample)
    print(f'Created a TChain object with {chain.GetEntries()} entries.')
    return chain

if __name__ == '__main__':
    tt = makechain()
    plotfactory.setpfstyle()
    can = ROOT.TCanvas('c1','c1')

    binsx = np.arange(0.,100.,5.)
    binsy = np.arange(0.,1.,0.1)

    hist = ROOT.TH2F('hist','hist',len(binsx)-1,binsx,len(binsy)-1,binsy)
    hist.SetTitle(';p_{T} (GeV); fakerate; entries')
    tt.Draw('ml_fr:l1_pt >> hist')
    hist.Draw('colz')

    # can.SetLogx()
    can.SetLogy()

    plotfactory.showlumi('59.7 fb^{-1} (13 TeV)')
    plotfactory.showlogopreliminary()

    can.Update()
    can.SaveAs('fakerateplots/fakerate_pt.pdf')
    set_trace()
