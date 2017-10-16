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
import versatiletrainer as train

def calculate_auc(allvolumes):
    '''
    Calculates AUC, or technically the concordance measure that is equivalent to AUC:
    for all pairs of volumes in different sets,
    how often is the predicted order == the real order?
    '''

    positive_class = []
    negative_class = []

    for vol in allvolumes:
        prediction = vol[8]
        realclass = vol[9]
        if realclass > 0.5:
            positive_class.append(prediction)
        else:
            negative_class.append(prediction)

    if len(positive_class) < 1 or len(negative_class) < 1:
        return 0

    comparisons = []

    for p in positive_class:
        for n in negative_class:
            if p > n:
                comparisons.append(1)
            elif p == n:
                comparisons.append(0.5)
            else:
                comparisons.append(0)

    return sum(comparisons) / len(comparisons)

def predictfic():

    ## PATHS.

    sourcefolder = '../sourcefiles/'
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

def genre_gridsearch(metadatapath, modelname, c_range, ftstart, ftend, ftstep, positive_tags = ['fic'], negative_tags = ['bio'], excl_below = 1700, excl_above = 2000):

    # Function does a gridsearch to identify an optimal number of features and setting of
    # the regularization constant; then produces that model.

    sourcefolder = '../sourcefiles/'
    extension = '.tsv'

    vocabpath = '../lexicons/' + modelname + '.txt'
    if os.path.exists(vocabpath):
        print('Vocabulary for ' + modelname + ' already exists. Using it.')
    outputpath = '../modeloutput/' + modelname + '.csv'

    # We can simply exclude volumes from consideration on the basis on any
    # metadata category we want, using the dictionaries defined below.

    ## EXCLUSIONS.

    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = excl_below
    excludeabove['firstpub'] = excl_above

    sizecap = 75

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


def predictbio():

    ## PATHS.

    sourcefolder = '../sourcefiles/'
    extension = '.tsv'
    metadatapath = '../metadata/hathigenremeta.csv'

    with open('../modeloutput/finalbiopredicts.csv', mode = 'w', encoding = 'utf-8') as f:
        f.write('center,accuracy,auc\n')

    for floor in range(1700, 2000, 20):
        if floor == 1720:
            continue
        if floor == 1700:
            ceiling = 1739
            center = 1720
        else:
            ceiling = floor + 19
            center = floor + 10

        modelname = 'cleanpredictbio' + str(floor)
        outputpath = '../modeloutput/' + modelname + str(datetime.date.today()) + '.csv'
        vocabpath = '../lexicons/' + modelname + '.csv'

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
        numfeatures = 1100
        regularization = .015

        paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

        for i in range(15):
            rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)
            auc = calculate_auc(allvolumes)

            print(floor, rawaccuracy, auc)
            with open('../modeloutput/finalbiopredicts.csv', mode = 'a', encoding = 'utf-8') as f:
                f.write(str(center) + ',' + str(rawaccuracy) + ',' + str(auc) + '\n')

            os.remove(vocabpath)
            # so that it gets recreated each time

def theninehundred():

    ## PATHS.

    sourcefolder = '../sourcefiles/'
    extension = '.tsv'
    metadatapath = '../metadata/hathigenremeta.csv'

    with open('../modeloutput/theninehundredpredicts.csv', mode = 'w', encoding = 'utf-8') as f:
        f.write('floor,accuracy,auc\n')


    for floor in range(1700, 2000, 50):
        ceiling = floor + 50

        modelname = 'theninehundred' + str(floor)
        outputpath = '../modeloutput/' + modelname + '.csv'
        vocabpath = '../lexicons/' + modelname + '.csv'

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
        numfeatures = 1100
        regularization = .00008

        paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)


        rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)

        auc = calculate_auc(allvolumes)
        print(floor, rawaccuracy, auc)
        with open('../modeloutput/theninehundredpredicts.csv', mode = 'a', encoding = 'utf-8') as f:
            f.write(str(floor + 25) + ',' + str(rawaccuracy) + ',' + str(auc) + '\n')

def predictecco():
    sourcefolder = '../sourcefiles/'
    extension = '.tsv'
    metadatapath = '../metadata/eccogenremeta.csv'

    modelname = 'predictecco'
    outputpath = '../modeloutput/' + modelname + str(datetime.date.today()) + '.csv'
    vocabpath = '../lexicons/' + modelname + '.csv'

    # We can simply exclude volumes from consideration on the basis on any
    # metadata category we want, using the dictionaries defined below.

    ## EXCLUSIONS.

    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 1800

    sizecap = 75

    # CLASSIFY CONDITIONS

    positive_tags = ['fic']
    negative_tags = ['bio']
    # testconditions = {'0', '2001', 'poe'}
    testconditions = set()

    datetype = "firstpub"
    numfeatures = 1100
    regularization = .015

    paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

    with open('../modeloutput/eccopredicts.csv', mode = 'w', encoding = 'utf-8') as f:
        f.write('row,accuracy,auc\n')

    for i in range(15):
        rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)
        auc = calculate_auc(allvolumes)

        print(i, rawaccuracy, auc)
        with open('../modeloutput/eccopredicts.csv', mode = 'a', encoding = 'utf-8') as f:
            f.write(str(i) + ',' + str(rawaccuracy) + ',' + str(auc) + '\n')

def oldpredictbio():

    ## PATHS.

    sourcefolder = '../sourcefiles/'
    extension = '.tsv'
    metadatapath = '../metadata/oldgenremeta2.csv'


    for floor in range(1700, 2000, 20):
        if floor == 1720:
            continue
        if floor == 1700:
            ceiling = 1739
            center = 1720
        else:
            ceiling = floor + 19
            center = floor + 10

        modelname = 'oldbio' + str(floor)
        outputpath = '../modeloutput/' + modelname + str(datetime.date.today()) + '.csv'
        vocabpath = '../lexicons/' + modelname + '.csv'

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
        numfeatures = 1100
        regularization = .015

        paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

        for i in range(7):
            rawaccuracy, allvolumes, coefficientuples = logisticpredict.create_model(paths, exclusions, classifyconditions)

            print(floor, rawaccuracy)
            with open('../modeloutput/oldbiopredicts.csv', mode = 'a', encoding = 'utf-8') as f:
                f.write(str(center) + ',' + str(rawaccuracy) + '\n')

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


if __name__ == '__main__':
    args = sys.argv
    command = args[1]

    if command == 'gridsearch':

        c_range = [.0012, .002, .004, .008, .015, 0.3, 0.8, 2, 10]
        featurestart = 800
        featureend = 2600
        featurestep = 100
        genre_gridsearch('../metadata/hathigenremeta.csv', 'tuningmodel', c_range, featurestart, featureend, featurestep)

    if command == 'useoldmeta':
        oldpredictbio()

    if command == 'usenewmeta':
        predictbio()

    if command == 'theninehundred':
        theninehundred()

    if command == 'predictecco':
        predictecco()

