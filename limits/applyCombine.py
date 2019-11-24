import os
import re
import multiprocessing
import time
from pdb import set_trace

def generateFileSetsDictionary():
    file_sets = {}
    for file in os.listdir("m12"):
        # extract mass and v2 from the file string
        mass = re.sub('.*_m_','',file)
        mass = re.sub('_.*','',mass)
        v2   = re.sub('.*_v2_','',file)
        v2   = re.sub('_.*','',v2)

        # extract displacement from the file string
        disp = None
        if    '_lt_0p5'      in file: disp = 'disp1'
        elif  '_0p5_to_2p0'  in file: disp = 'disp2'
        elif  '_mt_2p0'      in file: disp = 'disp3'
        else:
            print('cannot identify the displacement of m12/%s'%file) 

        # write the file path into the dictionary
        setName = 'm_%s_v2_%s'%(mass,v2)
        if setName not in file_sets: 
            file_sets[setName] = {}
        file_sets[setName][disp]='m12/'+file
    return file_sets

def convertDictToArray(file_sets_dict):
    file_sets_array = []
    for file_set_key in file_sets_dict:
        file_set_array = []

        #dictionaryKey
        file_set_array.append(file_set_key)

        #insert the three displacement locations
        file_set_array.append(file_sets_dict[file_set_key]['disp1'])
        file_set_array.append(file_sets_dict[file_set_key]['disp2'])
        file_set_array.append(file_sets_dict[file_set_key]['disp3'])
        
        #enter this as an element for the master input array
        file_sets_array.append(file_set_array)
    return file_sets_array


def combineCardsWrtDisplacement(inputData):
    disp1_path = inputData[1]
    disp2_path = inputData[2]
    disp3_path = inputData[3]

    output_path = 'combined/hnl_' + inputData[0] + '_majorana.txt' 
    combine_command = 'combineCards.py disp1=%s disp2=%s disp3=%s > %s'%(disp1_path,disp2_path,disp3_path,output_path) 

    print('start combining %s'%inputData[0]),
    os.system(combine_command)
    print('done!')
    return True

def runCombineCardsParallel(file_sets_array):
    n_sets = len(file_sets_array)
    n_CPU  = multiprocessing.cpu_count()
    print('running %d M/V2 sets on %d CPUs:'%(n_sets,n_CPU))
    start = time.time()
    pool    = multiprocessing.Pool(72)
    result  = pool.map(combineCardsWrtDisplacement,file_sets_array) 
    end = time.time()
    print('job done, it took %.2f seconds to combine'%(end-start))
    return True

def runCombine(inputDatacardArray):
    inputDataCard_path = inputDatacardArray[0]
    outputDir_path     = inputDatacardArray[1]
    mass = re.sub('.*_m_','',inputDataCard_path)
    mass = re.sub('_.*','',mass)
    v2   = re.sub('.*_v2_','',inputDataCard_path)
    v2   = re.sub('_.*','',v2)
    
    command = 'combine -M AsymptoticLimits %s --run blind > %s/m_%s_v2_%s.txt'%(inputDataCard_path,outputDir_path,mass,v2)
    print('running combine on M = %s; V2 = %s'%(mass,v2)),
    os.system(command)
    print('\t\tdone!')
    return True

def runCombineParallel():
    inputDatacardsArray = []
    for file in os.listdir("combined"):
        inputDataCard_path = 'combined/' + file 
        outputDir_path     = 'outputText'
        inputDatacardsArray.append([inputDataCard_path,outputDir_path])

    n_sets = len(inputDatacardsArray)
    n_CPU  = multiprocessing.cpu_count()
    print('running %d M/V2 sets on %d CPUs:'%(n_sets,n_CPU))
    start = time.time()
    pool    = multiprocessing.Pool(72)
    result  = pool.map(runCombine,inputDatacardsArray) 
    end = time.time()
    print('job done, it took %.2f seconds to combine'%(end-start))
    return True

def combineTxtFiles():
    output_file = open('output.txt','w')
    for file in os.listdir('outputText'):
        with open('outputText/'+file, 'r') as f_in:
            for line in f_in:
                output_file.write(line)
    output_file.close()

if __name__ == '__main__':

    # # prepare the input data for combine
    # file_sets_dict  = generateFileSetsDictionary()
    # file_sets_array = convertDictToArray(file_sets_dict)

    # # combining displ cards using multiprocess
    # # one can substitute file_sets_array with a smaller one for testing
    # runCombineCardsParallel(file_sets_array)

    # # run combine with all available cpus!
    # runCombineParallel()


    # # add all the output files together
    combineTxtFiles()

    

    

    ## for testing!
    # testSet = file_sets_array[0]
    # combineCardsInDisplacement(testSet)
    # testArray = [file_sets_array[0],file_sets_array[1],file_sets_array[2]]
    # result  = pool.map(combineCardsWrtDisplacement,testArray) 

