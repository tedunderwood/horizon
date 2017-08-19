#!/usr/bin/env python3

# reproduce_fictional_prestige.py

# Scripts to reproduce models
# used in Chapter Three,
# The Directions of Literary Change.

import csv, os, sys, pickle, math

# we add a path to be searched so that we can import
# versatiletrainer, which will do most of the work
# Versatiletrainer, and the modules it will in turn call,
# are publicly available in this github repo:
# https://github.com/tedunderwood/overlappingcategories

# mental note: when you file the book repo with Zenodo,
# a copy of the overlappingcategories repo also needs to
# be frozen

sys.path.append('/Users/tunder/Dropbox/python/logistic')
import versatiletrainer as train

import pandas as pd

    # sourcefolder =
    # extension =
    # metadatapath =
    # outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/predictions.csv'

def genre_gridsearch(metadatapath, modelname, c_range, ftstart, ftend, ftstep, positive_tags = ['elite'], negative_tags = ['vulgar'], excl_below = 1700, excl_above = 2000):

    # Function does a gridsearch to identify an optimal number of features and setting of
    # the regularization constant; then produces that model.

    # sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/fromEF/'
    sourcefolder = '../sourcefiles/'
    extension = '.tsv'
    #metadatapath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/prestigeficmeta.csv'

    vocabpath = '/Users/tunder/Dropbox/fiction/lexicon/' + modelname + '.txt'
    if os.path.exists(vocabpath):
        print('Vocabulary for ' + modelname + ' already exists. Using it.')
    outputpath = '../results/' + modelname + '.csv'

    # We can simply exclude volumes from consideration on the basis on any
    # metadata category we want, using the dictionaries defined below.

    ## EXCLUSIONS.

    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = excl_below
    excludeabove['firstpub'] = excl_above

    sizecap = 700

    # CLASSIFY CONDITIONS

    # print()
    # print("You can also specify positive tags to be excluded from training, and/or a pair")
    # print("of integer dates outside of which vols should be excluded from training.")
    # print("If you add 'donotmatch' to the list of tags, these volumes will not be")
    # print("matched with corresponding negative volumes.")
    # print()
    # ## testphrase = input("Comma-separated list of such tags: ")
    testphrase = ''
    testconditions = set([x.strip() for x in testphrase.split(',') if len(x) > 0])

    datetype = "firstpub"
    numfeatures = ftend
    regularization = .000075
    # linting the code would get rid of regularization, which is at this
    # point an unused dummy parameter

    paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

    modelparams = 'logistic', 12, ftstart, ftend, ftstep, c_range

    matrix, rawaccuracy, allvolumes, coefficientuples = train.tune_a_model(paths, exclusions, classifyconditions, modelparams)

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))
    tiltaccuracy = train.diachronic_tilt(allvolumes, 'linear', [])

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

def applymodel(modelpath, metadatapath, outpath):
    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/fromEF'
    extension = '.tsv'
    newmetadict = train.apply_pickled_model(modelpath, sourcefolder, extension, metadatapath)
    print('Got predictions for that model.')
    newmetadict.to_csv(outpath)

def comparison(selfmodel, othermodel, modelname):

        totalvolumes = 0
        right = 0

        for v in selfmodel.index:
            realgenre = selfmodel.loc[v, 'realclass']
            v = str(v)
            otherprediction = othermodel.loc[v, modelname]
            if realgenre > .5 and otherprediction > 0.5:
                right += 1
            elif realgenre < .5 and otherprediction < 0.5:
                right += 1
            totalvolumes +=1

        return totalvolumes, right

def getacc(filelist):
    allofem = 0
    allright = 0
    for afile in filelist:
        df = pd.read_csv(afile)
        totalcount = len(df.realclass)
        tp = sum((df.realclass > 0.5) & (df.logistic > 0.5))
        tn = sum((df.realclass <= 0.5) & (df.logistic <= 0.5))
        fp = sum((df.realclass <= 0.5) & (df.logistic > 0.5))
        fn = sum((df.realclass > 0.5) & (df.logistic <= 0.5))
        assert totalcount == (tp + fp + tn + fn)
        allofem += totalcount
        allright += (tp + tn)
    return allright / allofem

if __name__ == '__main__':

    args = sys.argv
    command = args[1]

    if command == 'littlemagazines':

        c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
        featurestart = 1500
        featureend = 4000
        featurestep = 100
        genre_gridsearch('/Users/tunder/Dropbox/GenreProject/python/reception/fiction/littlemagazines.csv', 'littlemagazinespost1919', c_range, featurestart, featureend, featurestep, positive_tags = ['elite'], negative_tags = ['vulgar'], excl_below = 1800, excl_above = 2000)

    elif command == 'apply_quarter_century_models':

        # We've previously trained models for each quarter-century
        # of the fiction corpus: 1850-74, 75-99, and so on.
        # Now we need to apply those models to the whole corpus
        # in order to see how good their predictions are.

        models = []
        outpaths = []
        for i in range (1850, 1950, 25):
            modelpath = '../models/segment' + str(i) + '.pkl'
            models.append(modelpath)
            outpath = '../results/segment' + str(i) + '.applied.csv'
            outpaths.append(outpath)
        metadatapath = '../metadata/prestigeficmeta.csv'
        for m, o in zip(models, outpaths):
            applymodel(m, metadatapath, o)

    elif command == 'gender_balance_fiction':

        c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
        featurestart = 1200
        featureend = 4500
        featurestep = 100
        genre_gridsearch('../metadata/genderbalancedfiction.csv', 'gender_balanced_fiction', c_range, featurestart, featureend, featurestep, positive_tags = ['elite'], negative_tags = ['vulgar'], excl_below = 1800, excl_above = 2000)

    elif command == 'nation_balance_fiction':

        c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
        featurestart = 1200
        featureend = 4000
        featurestep = 100
        genre_gridsearch('../metadata/nationbalancedfiction.csv', 'nation_balanced_fiction', c_range, featurestart, featureend, featurestep, positive_tags = ['elite'], negative_tags = ['vulgar'], excl_below = 1800, excl_above = 2000)



