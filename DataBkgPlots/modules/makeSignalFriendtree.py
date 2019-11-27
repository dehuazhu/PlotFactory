import ROOT
from array import array
from modules.ReweightBranchNames import ReweightBranchNames
import re
import os
from pdb import set_trace

class Branch:
    def __init__(self, name, value, tag):
        self.name   = name
        self.value  = value
        self.tag    = tag


def makeSignalFriendtree(treeFilePath):
    treeFile        = ROOT.TFile(treeFilePath + 'tree.root')
    tree            = treeFile.Get('tree')
    NumberOfEvents  = tree.GetEntries()

    newTreeFile     = ROOT.TFile(treeFilePath + 'tree_with_p_instead_of_dot.root','RECREATE')
    newTree         = tree.CloneTree(0)

    Branches = {}
    for reweightBranchName in ReweightBranchNames:
        name    = reweightBranchName
        value   = array('d',[0])
        tag     = (reweightBranchName + '/D') 
        Branches[reweightBranchName]={}
        Branches[reweightBranchName]['BranchObject'] = Branch(
                name    = name,
                value   = value,
                tag     = tag, 
                )
        Branches[reweightBranchName]['TBranchObject'] = newTree.Branch(name,Branches[reweightBranchName]['BranchObject'].value,tag)

    for currentEvent in range(NumberOfEvents):
        tree.GetEntry(currentEvent)
        for reweightBranchName in ReweightBranchNames:
            currentBranch = Branches[reweightBranchName]
            reweightBranchNameWithDot = re.sub('p','.',reweightBranchName)
            try:
                value = tree.GetLeaf(reweightBranchNameWithDot).GetValue()
                currentBranch['BranchObject'].value[0] = value
            except:
                print('event %d: No value found for branch %s'%(currentEvent,reweightBranchName))
                set_trace()
                continue
            # if reweightBranchName == 'xs_w_v2_2p0em04': set_trace()
        newTree.Fill()

    newTree.Write()
    print('made new friendtree at path: %s'%(treeFilePath))
    return True

def makeSignalFriendtrees(parentDirectory):

    sampleDirectories = [x[0] for x in os.walk(parentDirectory)]
    channels = ['mmm','mem','eee','eem']

    for sampleDirectory in sampleDirectories:
        if 'HNLTreeProducer' not in sampleDirectory: continue
        treeDirectory = sampleDirectory + '/'
        hasTree = os.path.isfile(treeDirectory + 'tree.root') 
        if hasTree: 
            try:
                makeSignalFriendtree(treeDirectory)
            except:
                print('ERROR at %s'%treeDirectory)
                continue

    return True

if __name__ == '__main__':
    # treeFilePath = '/mnt/StorageElement1/4_production/2018/production_20191126_Signal_mmm/signals_2018/HN3L_M_5_V_0p000316227766017_mu_massiveAndCKM_LO/HNLTreeProducer_mmm/'
    # makeSignalFriendtree(treeFilePath = treeFilePath)

    parentDirectory = '/mnt/StorageElement1/4_production/2018/production_20191126_Signal_mmm/signals_2018/'
    makeSignalFriendtrees(parentDirectory)
