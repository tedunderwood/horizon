#!/usr/bin/env python3

# reproduce_poetic_prestige.py

# Scripts to recreate models used in
# Chapter 3, Directions of Literary Change.

import csv, os, sys, pickle, math
import pandas as pd

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

def genre_gridsearch(metadatapath, modelname, c_range, ftstart, ftend, ftstep, positive_tags = ['elite'], negative_tags = ['vulgar'], excl_below = 1700, excl_above = 2000):
    # Function does a gridsearch to identify an optimal number of features and setting of
    # the regularization constant; then produces that model.

    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/poetryEF/fromEF/'
    extension = '.tsv'
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
    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/poetryEF/fromEF'
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

    if len(args) < 2:

        c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
        featurestart = 1500
        featureend = 4000
        featurestep = 100
        genre_gridsearch('/Users/tunder/Dropbox/book/chapter3/metadata/prestigepoemeta.csv', 'poeEF2', c_range, featurestart, featureend, featurestep, positive_tags = ['reviewed'], negative_tags = ['random'], excl_below = 1800, excl_above = 2000)

    elif command == 'train_quarter_century_models':
        for i in range (1820, 1920, 25):
                c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
                featurestart = 1300
                featureend = 4400
                featurestep = 100
                modelname = 'poe_quarter_'+str(i)
                genre_gridsearch('../results/prestigepoemeta.csv', modelname, c_range, featurestart, featureend, featurestep, positive_tags = ['reviewed'], negative_tags = ['random'], excl_below = i, excl_above = i + 24)

    elif command == 'poetry_post_1845':
        c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
        featurestart = 3000
        featureend = 5500
        featurestep = 100
        modelname = 'poetry_post_1845'
        genre_gridsearch('../results/prestigepoemeta.csv', modelname, c_range, featurestart, featureend, featurestep, positive_tags = ['reviewed'], negative_tags = ['random'], excl_below = 1845, excl_above = 2000)

    elif command == 'apply_quarter_century_models':

        # We've previously trained models for each quarter-century
        # of the poetry corpus: 1850-74, 75-99, and so on.
        # Now we need to apply those models to the whole corpus
        # in order to see how good their predictions are.

        models = []
        outpaths = []
        for i in range (1820, 1920, 25):
            modelpath = '../models/poe_quarter_' + str(i) + '.pkl'
            models.append(modelpath)
            outpath = '../results/poe_quarter_' + str(i) +'.applied.csv'
            outpaths.append(outpath)
        metadatapath = '../metadata/prestigepoemeta.csv'
        for m, o in zip(models, outpaths):
            applymodel(m, metadatapath, o)

    elif command == 'gender_balance_poetry':

        c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
        featurestart = 1200
        featureend = 4200
        featurestep = 100
        genre_gridsearch('../metadata/genderbalancedpoetry.csv', 'gender_balanced_poetry', c_range, featurestart, featureend, featurestep, positive_tags = ['reviewed'], negative_tags = ['random'], excl_below = 1800, excl_above = 2000)

    elif command == 'nation_balance_poetry':

        c_range = [.00009, .0002, .0004, .0008, .0012, .002, .004, .008, .012, 0.3, 0.8, 2]
        featurestart = 1200
        featureend = 4200
        featurestep = 100
        genre_gridsearch('../metadata/nationbalancedpoetry.csv', 'nation_balanced_poetry', c_range, featurestart, featureend, featurestep, positive_tags = ['reviewed'], negative_tags = ['random'], excl_below = 1800, excl_above = 2000)

