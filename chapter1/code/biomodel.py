#!/usr/bin/env python3

# biomodel.py

# modeling biography and fiction

# NOTE: this code needs some editing to actually run in the repo.
# Paths need to be changed to point to the copies of allgenremeta
# and subsetmeta in chapter1/metadata, and to point to sourcefiles
# instead of allgenremeta.

# But this is code that *produced* the models in chapter 1.
# Specifically the function predictbio() produced biopredictsII.csv,
# and the function predictparts() produced allsubset2.csv.

# Note that it calls logisticpredict from the /logistic folder
# of the master book repo.

import csv, os, sys, random, datetime
from collections import Counter

# import utils
sys.path.append('../../logistic/')

import logisticpredict

def main():

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/python/nonfic/allgenres/'
    extension = '.tsv'
    metadatapath = 'subsetmeta.csv'
    vocabpath = 'vocab/subsetvocab.txt'

    modelname = 'subsetmodelfull'
    outputpath = '../results/' + modelname + str(datetime.date.today()) + '.csv'

    # We can simply exclude volumes from consideration on the basis on any
    # metadata category we want, using the dictionaries defined below.

    ## EXCLUSIONS.

    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 2000

    # We have to explicitly exclude genres because the category "stew" in the
    # positive category wouldn't otherwise automatically exclude the constituent
    # tags that were used to create it.

    # I would just have put all those tags in the positive tag list, but then you'd lose
    # the ability to explicitly balance equal numbers of crime, gothic,
    # and science fiction, plus sensation novels. You'd get a list dominated by
    # the crime categories, which are better-represented in the dataset.

    sizecap = 400

    # CLASSIFY CONDITIONS

    # We ask the user for a list of categories to be included in the positive
    # set, as well as a list for the negative set. Default for the negative set
    # is to include all the "random"ly selected categories. Note that random volumes
    # can also be tagged with various specific genre tags; they are included in the
    # negative set only if they lack tags from the positive set.

    positive_tags = ['fic']
    negative_tags = ['bio']
    # testconditions = {'0', '2001', 'poe', 'limit==250'}
    testconditions = set()

    datetype = "firstpub"
    numfeatures = 3200
    regularization = .00008

    paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

    rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))

    tiltaccuracy = logisticpredict.diachronic_tilt(allvolumes, 'linear', [])

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

    return allvolumes

def predictpoe():

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/python/nonfic/allgenres/'
    extension = '.tsv'
    metadatapath = 'allgenremeta.csv'

    for floor in range(1700, 1900, 20):
        ceiling = floor + 19

        modelname = 'predictpoe' + str(floor)
        outputpath = '../results/' + modelname + str(datetime.date.today()) + '.csv'
        vocabpath = 'vocab/predictvocab' + str(floor) + '.txt'

        # We can simply exclude volumes from consideration on the basis on any
        # metadata category we want, using the dictionaries defined below.

        ## EXCLUSIONS.

        excludeif = dict()
        excludeifnot = dict()
        excludeabove = dict()
        excludebelow = dict()

        excludebelow['firstpub'] = floor
        excludeabove['firstpub'] = ceiling

        # We have to explicitly exclude genres because the category "stew" in the
        # positive category wouldn't otherwise automatically exclude the constituent
        # tags that were used to create it.

        # I would just have put all those tags in the positive tag list, but then you'd lose
        # the ability to explicitly balance equal numbers of crime, gothic,
        # and science fiction, plus sensation novels. You'd get a list dominated by
        # the crime categories, which are better-represented in the dataset.

        sizecap = 100

        # CLASSIFY CONDITIONS

        # We ask the user for a list of categories to be included in the positive
        # set, as well as a list for the negative set. Default for the negative set
        # is to include all the "random"ly selected categories. Note that random volumes
        # can also be tagged with various specific genre tags; they are included in the
        # negative set only if they lack tags from the positive set.

        positive_tags = ['poe', 'fic']
        negative_tags = ['bio']
        testconditions = {'0', '2001', 'poe'}
        # testconditions = set()

        datetype = "firstpub"
        numfeatures = 3200
        regularization = .00008

        paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

        rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)


        allpoe = 0
        rightpoe = 0
        for vol in allvolumes:
            if vol[14] == 'poe':
                allpoe += 1
                if vol[8] > 0.5:
                    rightpoe += 1

        recall = (rightpoe / allpoe)
        print(floor, recall)
        with open('../results/poepredicts.csv', mode = 'a', encoding = 'utf-8') as f:
            f.write(str(floor) + ',' + str(recall) + '\n')

def predictfic():

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/python/nonfic/allgenres/'
    extension = '.tsv'
    metadatapath = 'allgenremeta.csv'

    for floor in range(1720, 1920, 10):
        ceiling = floor + 19

        modelname = 'predictfic' + str(floor)
        outputpath = '../results/' + modelname + str(datetime.date.today()) + '.csv'
        vocabpath = 'vocab/predictfic' + str(floor) + '.txt'

        # We can simply exclude volumes from consideration on the basis on any
        # metadata category we want, using the dictionaries defined below.

        ## EXCLUSIONS.

        excludeif = dict()
        excludeifnot = dict()
        excludeabove = dict()
        excludebelow = dict()

        excludebelow['firstpub'] = floor
        excludeabove['firstpub'] = ceiling

        # We have to explicitly exclude genres because the category "stew" in the
        # positive category wouldn't otherwise automatically exclude the constituent
        # tags that were used to create it.

        # I would just have put all those tags in the positive tag list, but then you'd lose
        # the ability to explicitly balance equal numbers of crime, gothic,
        # and science fiction, plus sensation novels. You'd get a list dominated by
        # the crime categories, which are better-represented in the dataset.

        sizecap = 100

        # CLASSIFY CONDITIONS

        # We ask the user for a list of categories to be included in the positive
        # set, as well as a list for the negative set. Default for the negative set
        # is to include all the "random"ly selected categories. Note that random volumes
        # can also be tagged with various specific genre tags; they are included in the
        # negative set only if they lack tags from the positive set.

        positive_tags = ['fic']
        negative_tags = ['bio']
        #testconditions = {'0', '2001', 'poe'}
        testconditions = set()

        datetype = "firstpub"
        numfeatures = 3000
        regularization = .00008

        paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

        rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)

        with open('../results/ficpredicts.csv', mode = 'a', encoding = 'utf-8') as f:
            f.write(str(floor) + ',' + str(rawaccuracy) + '\n')

def predictbio():

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/python/nonfic/allgenres/'
    extension = '.tsv'
    metadatapath = 'allgenremeta.csv'

    for floor in range(1700, 2000, 30):
        ceiling = floor + 29

        modelname = 'predictmutablevocab' + str(floor)
        outputpath = '../results/' + modelname + str(datetime.date.today()) + '.csv'
        vocabpath = 'vocab/biovfic3centuryIII.txt'

        # We can simply exclude volumes from consideration on the basis on any
        # metadata category we want, using the dictionaries defined below.

        ## EXCLUSIONS.

        excludeif = dict()
        excludeifnot = dict()
        excludeabove = dict()
        excludebelow = dict()

        excludebelow['firstpub'] = floor
        excludeabove['firstpub'] = ceiling

        # We have to explicitly exclude genres because the category "stew" in the
        # positive category wouldn't otherwise automatically exclude the constituent
        # tags that were used to create it.

        # I would just have put all those tags in the positive tag list, but then you'd lose
        # the ability to explicitly balance equal numbers of crime, gothic,
        # and science fiction, plus sensation novels. You'd get a list dominated by
        # the crime categories, which are better-represented in the dataset.

        sizecap = 75

        # CLASSIFY CONDITIONS

        # We ask the user for a list of categories to be included in the positive
        # set, as well as a list for the negative set. Default for the negative set
        # is to include all the "random"ly selected categories. Note that random volumes
        # can also be tagged with various specific genre tags; they are included in the
        # negative set only if they lack tags from the positive set.

        positive_tags = ['fic']
        negative_tags = ['bio']
        # testconditions = {'0', '2001', 'poe'}
        testconditions = set()

        datetype = "firstpub"
        numfeatures = 3200
        regularization = .00008

        paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

        for i in range(15):
            rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)

            print(floor, rawaccuracy)
            with open('../results/biopredictsIII.csv', mode = 'a', encoding = 'utf-8') as f:
                f.write(str(floor) + ',' + str(rawaccuracy) + '\n')

            os.remove(vocabpath)
            # so that it gets recreated each time

def predict2017test():

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/python/nonfic/2017test/'
    extension = '.tsv'
    metadatapath = '2017testmeta.csv'

    vocabpath = 'vocab/2017testvocab.txt'

    modelname = '2017testmodel'
    outputpath = '../results/' + modelname + str(datetime.date.today()) + '.csv'

    # We can simply exclude volumes from consideration on the basis on any
    # metadata category we want, using the dictionaries defined below.

    ## EXCLUSIONS.

    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 2000

    # We have to explicitly exclude genres because the category "stew" in the
    # positive category wouldn't otherwise automatically exclude the constituent
    # tags that were used to create it.

    # I would just have put all those tags in the positive tag list, but then you'd lose
    # the ability to explicitly balance equal numbers of crime, gothic,
    # and science fiction, plus sensation novels. You'd get a list dominated by
    # the crime categories, which are better-represented in the dataset.

    sizecap = 400

    # CLASSIFY CONDITIONS

    # We ask the user for a list of categories to be included in the positive
    # set, as well as a list for the negative set. Default for the negative set
    # is to include all the "random"ly selected categories. Note that random volumes
    # can also be tagged with various specific genre tags; they are included in the
    # negative set only if they lack tags from the positive set.

    positive_tags = ['fic']
    negative_tags = ['bio']
    # testconditions = {'0', '2001', 'poe', 'limit==250'}
    testconditions = set()

    datetype = "firstpub"
    numfeatures = 3200
    regularization = .00008

    paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

    rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))

    tiltaccuracy = logisticpredict.diachronic_tilt(allvolumes, 'linear', [])

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

    return allvolumes

def predict_parts():

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/python/nonfic/allgenres/'
    extension = '.tsv'
    metadatapath = 'subsetmeta.csv'

    for floor in range(1700, 2000, 50):
        ceiling = floor + 49

        modelname = 'subsetVpart2' + str(floor)
        outputpath = '../results/' + modelname + str(datetime.date.today()) + '.csv'
        # vocabpath = 'vocab/predictbiovocabII' + str(floor) + '.txt'
        vocabpath = 'vocab/subsetvocab2' + str(floor) + '.txt'

        # We can simply exclude volumes from consideration on the basis on any
        # metadata category we want, using the dictionaries defined below.

        ## EXCLUSIONS.

        excludeif = dict()
        excludeifnot = dict()
        excludeabove = dict()
        excludebelow = dict()

        excludebelow['firstpub'] = floor
        excludeabove['firstpub'] = ceiling

        # We have to explicitly exclude genres because the category "stew" in the
        # positive category wouldn't otherwise automatically exclude the constituent
        # tags that were used to create it.

        # I would just have put all those tags in the positive tag list, but then you'd lose
        # the ability to explicitly balance equal numbers of crime, gothic,
        # and science fiction, plus sensation novels. You'd get a list dominated by
        # the crime categories, which are better-represented in the dataset.

        sizecap = 100

        # CLASSIFY CONDITIONS

        # We ask the user for a list of categories to be included in the positive
        # set, as well as a list for the negative set. Default for the negative set
        # is to include all the "random"ly selected categories. Note that random volumes
        # can also be tagged with various specific genre tags; they are included in the
        # negative set only if they lack tags from the positive set.

        positive_tags = ['fic']
        negative_tags = ['bio']
        # testconditions = {'0', '2001', 'poe'}
        testconditions = set()

        datetype = "firstpub"
        numfeatures = 3200
        regularization = .00008

        paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)


        rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)

        print(floor, rawaccuracy)

if __name__ == '__main__':
    # allvolumes = main()
    # predict_parts()
    predict2017test()
