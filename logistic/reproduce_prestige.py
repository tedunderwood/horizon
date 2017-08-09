#!/usr/bin/env python3

# reproduce.py

import csv, os, sys, pickle, math

import versatiletrainer as train

import pandas as pd

    # sourcefolder =
    # extension =
    # metadatapath =
    # outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/predictions.csv'

def genre_gridsearch(modelname, c_range, ftstart, ftend, ftstep, positive_tags = ['elite'], negative_tags = ['vulgar'], excl_below = 1700, excl_above = 2000):
    # Function does a gridsearch to identify an optimal number of features and setting of
    # the regularization constant; then produces that model.

    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/fromEF/'
    extension = '.tsv'
    #metadatapath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/prestigeficmeta.csv'
    metadatapath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/littlemagazines.csv'
    vocabpath = '/Users/tunder/Dropbox/fiction/lexicon/' + modelname + '.txt'
    if os.path.exists(vocabpath):
        print('Vocabulary for ' + modelname + ' already exists. Using it.')
    outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/' + modelname + '.csv'

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

def applymodel():
    modelpath = input('Path to model? ')
    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/fromEF'
    extension = '.tsv'
    metadatapath = 'mergedmeta.csv'
    newmetadict = train.apply_pickled_model(modelpath, sourcefolder, extension, metadatapath)
    print('Got predictions for that model.')
    outpath = 'mergedmeta.csv'
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

    if len(args) < 2:

        c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
        featurestart = 1500
        featureend = 4000
        featurestep = 100
        genre_gridsearch('littlemagazinespost1919', c_range, featurestart, featureend, featurestep, positive_tags = ['elite'], negative_tags = ['vulgar'], excl_below = 1800, excl_above = 2000)
