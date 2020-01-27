from __future__ import print_function
import os
from pdb import set_trace
import re

def makeCombinedDataCards(channel, output_folder, in_folder_XXX, in_folder_Xem_OS, in_folder_Xem_SS):
    fileNamesXXX    = sorted(os.listdir(in_folder_XXX))
    fileNamesXem_OS = sorted(os.listdir(in_folder_Xem_OS))
    fileNamesXem_SS = sorted(os.listdir(in_folder_Xem_SS))

    for i, fileNameXXX in enumerate(fileNamesXXX):

        # make sure that we're talking about the same sample
        if channel == 'm': fileNameBase = re.sub('mmm.txt','',fileNameXXX)
        if channel == 'e': fileNameBase = re.sub('eee.txt','',fileNameXXX)
        if (fileNameBase not in fileNamesXem_OS[i]) or (fileNameBase not in fileNamesXem_SS[i]): 
            set_trace()
            continue

        filePathXXX     = in_folder_XXX       + fileNameXXX
        filePathXem_OS  = in_folder_Xem_OS    + fileNamesXem_OS[i]
        filePathXem_SS  = in_folder_Xem_SS    + fileNamesXem_SS[i]
        outputFilePath  = output_folder       + fileNameBase + 'm.txt'


        command = 'combineCards.py %s%s%s=%s %sem_OS=%s %sem_SS=%s > %s'%(channel,channel,channel,filePathXXX, channel, filePathXem_OS, channel, filePathXem_SS, outputFilePath)
        os.system(command)
        print('[job %d/%d]: finished combining %s'%(i,len(fileNamesXXX),fileNameBase),end='\r'),
    return True
    



if __name__ == '__main__':
    channels = []
    # channels.append('m')
    channels.append('e')

    # datacardVersion = '20191129_NewDispBin'
    datacardVersion = '20200123_AN_Feb'
    for channel in channels:
        #new 2018
        if channel == 'm':
            in_folder_XXX    = '/work/dezhu/3_figures/2_Limits/2018/%smm/%s/datacards/'%(channel,datacardVersion)
        if channel == 'e':
            in_folder_XXX    = '/work/dezhu/3_figures/2_Limits/2018/%see/%s/datacards/'%(channel,datacardVersion)

        in_folder_Xem_OS = '/work/dezhu/3_figures/2_Limits/2018/%sem_OS/%s/datacards/'%(channel,datacardVersion)
        in_folder_Xem_SS = '/work/dezhu/3_figures/2_Limits/2018/%sem_SS/%s/datacards/'%(channel,datacardVersion)

        output_base = '/work/dezhu/3_figures/2_Limits/2018/%sCombined/%s'%(channel[0],datacardVersion)
        
        output_folder = output_base + '/datacards/'

        if not os.path.isdir(output_base): os.mkdir(output_base)
        if not os.path.isdir(output_folder): os.mkdir(output_folder)

        makeCombinedDataCards(channel, output_folder, in_folder_XXX, in_folder_Xem_OS, in_folder_Xem_SS)
        print('done')
        
