#!/usr/bin/env python3

# reproduce.py

import csv, os, sys, pickle, math

import versatiletrainer as train

import pandas as pd

def basic_svm_gridsearch():
    # If this class is called directly, it creates a single model using the default
    # settings set below.

    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/fromEF'
    extension = '.tsv'
    metadatapath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/snootymeta.csv'
    vocabpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/lexica/snootylexicon.txt'

    ## modelname = input('Name of model? ')
    modelname = 'second'

    outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/results/' + modelname + str(datetime.date.today()) + '.csv'

    # We can simply exclude volumes from consideration on the basis on any
    # metadata category we want, using the dictionaries defined below.

    ## EXCLUSIONS.

    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    ## daterange = input('Range of dates to use in the model? ')
    daterange = '1850,1950'
    if ',' in daterange:
        dates = [int(x.strip()) for x in daterange.split(',')]
        dates.sort()
        if len(dates) == 2:
            assert dates[0] < dates[1]
            excludebelow['firstpub'] = dates[0]
            excludeabove['firstpub'] = dates[1]

    sizecap = 200

    # CLASSIFY CONDITIONS

    # We ask the user for a list of categories to be included in the positive
    # set, as well as a list for the negative set. Default for the negative set
    # is to include all the "random"ly selected categories. Note that random volumes
    # can also be tagged with various specific genre tags; they are included in the
    # negative set only if they lack tags from the positive set.

    ## tagphrase = input("Comma-separated list of tags to include in the positive class: ")
    tagphrase = 'elite'
    positive_tags = [x.strip() for x in tagphrase.split(',')]
    ## tagphrase = input("Comma-separated list of tags to include in the negative class: ")
    tagphrase = 'vulgar'

    # An easy default option.
    if tagphrase == 'r':
        negative_tags = ['random', 'grandom', 'chirandom']
    else:
        negative_tags = [x.strip() for x in tagphrase.split(',')]

    # We also ask the user to specify categories of texts to be used only for testing.
    # These exclusions from training are in addition to ordinary crossvalidation.

    print()
    print("You can also specify positive tags to be excluded from training, and/or a pair")
    print("of integer dates outside of which vols should be excluded from training.")
    print("If you add 'donotmatch' to the list of tags, these volumes will not be")
    print("matched with corresponding negative volumes.")
    print()
    ## testphrase = input("Comma-separated list of such tags: ")
    testphrase = ''
    testconditions = set([x.strip() for x in testphrase.split(',') if len(x) > 0])

    datetype = "firstpub"
    numfeatures = 5000
    regularization = .000075

    paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

    c_range = [.00008, .0001, .00012, .00013, .00014, .00016, .00018]

    modelparams = 'svm', 10, 3600, 3900, 50, c_range

    matrix, rawaccuracy, allvolumes, coefficientuples = tune_a_model(paths, exclusions, classifyconditions, modelparams)

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))
    tiltaccuracy = diachronic_tilt(allvolumes, 'linear', [])

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

def genre_gridsearch(modelname, c_range, ftstart, ftend, ftstep, positive_tags, negative_tags = ['random', 'grandom', 'chirandom'], excl_below = 1700, excl_above = 2000):
    # Function does a gridsearch to identify an optimal number of features and setting of
    # the regularization constant; then produces that model.

    sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
    extension = '.tsv'
    metadatapath = '/Users/tunder/Dropbox/fiction/meta/concatenatedmeta.csv'
    vocabpath = '/Users/tunder/Dropbox/fiction/lexicon/' + modelname + '.txt'
    if os.path.exists(vocabpath):
        print('Vocabulary for ' + modelname + ' already exists. Using it.')
    outputpath = '/Users/tunder/Dropbox/fiction/results/' + modelname + '.csv'

    # We can simply exclude volumes from consideration on the basis on any
    # metadata category we want, using the dictionaries defined below.

    ## EXCLUSIONS.

    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = excl_below
    excludeabove['firstpub'] = excl_above

    sizecap = 400

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

    modelparams = 'logistic', 10, ftstart, ftend, ftstep, c_range

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
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100', 'newgate']
        c_range = [.001, .003, .01, .03, .1, .3, 1]
        featurestart = 3400
        featureend = 4200
        featurestep = 100
        genre_gridsearch('testnewgate', c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'det100only':
        modelname = 'det100only'
        positive_tags = ['det100']
        c_range = [.001, .003, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 5000
        featurestep = 250
        genre_gridsearch('det100only', c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'locdetective':
        modelname = 'locdetective'
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst']
        c_range = [.001, .003, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 5250
        featurestep = 250
        genre_gridsearch('locdetective', c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'alldetective':
        modelname = 'alldetective'
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 3000
        featureend = 4400
        featurestep = 50
        genre_gridsearch('alldetective', c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'compare':
        # This routine assumes that you have already trained models for classes A and B.
        # It compares them.
        firstmodel = args[2]
        secondmodel = args[3]
        firstpath = '/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.pkl'
        secondpath = '/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.pkl'
        metadatapath = '/Users/tunder/Dropbox/fiction/meta/concatenatedmeta.csv'
        sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
        extension = '.tsv'
        firstonall = train.apply_pickled_model(firstpath, sourcefolder, extension, metadatapath)
        # firstonall.set_index('docid', inplace = True)
        secondonall = train.apply_pickled_model(secondpath, sourcefolder, extension, metadatapath)
        # secondonall.set_index('docid', inplace = True)
        firstonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.csv', index_col = 'volid')
        secondonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.csv', index_col = 'volid')

        firsttotal, firstright = comparison(firstonself, secondonall, secondmodel)
        secondtotal, secondright = comparison(secondonself, firstonall, firstmodel)

        print(firsttotal, firstright)
        print("Accuracy of " + secondmodel + " on volumes originally included in "+ firstmodel + ": " + str(firstright/firsttotal))
        print(secondtotal, secondright)
        print("Accuracy of " + firstmodel + " on volumes originally included in "+ secondmodel + ": " + str(secondright/secondtotal))
        print("Total accuracy: ", (firstright + secondright) / (firsttotal + secondtotal))

    elif args[1] == 'restricteddetective':
        modelname = 'restricteddetective'
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 50
        featureend = 120
        featurestep = 10
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'restrictedSF':
        modelname = 'restricteddSF'
        positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 50
        featureend = 120
        featurestep = 10
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'alldetectivepre1915':
        modelname = 'alldetectivepre1915'
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2900
        featureend = 4600
        featurestep = 100
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags,negative_tags = ['random', 'grandom', 'chirandom'], excl_below = 1700, excl_above = 1914)

    elif args[1] == 'alldetectivepost1914':
        modelname = 'alldetectivepost1914'
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2900
        featureend = 4600
        featurestep = 100
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags,negative_tags = ['random', 'grandom', 'chirandom'], excl_below = 1915, excl_above = 2000)

    elif args[1] == 'alldetectivepost1960':
        modelname = 'alldetectivepost1914'
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2900
        featureend = 4600
        featurestep = 100
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags,negative_tags = ['random', 'grandom', 'chirandom'], excl_below = 1960, excl_above = 2000)

    elif args[1] == 'newgateonly':
        modelname = args[1]
        positive_tags = ['newgate']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 4800
        featurestep = 200
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'sensation':
        modelname = args[1]
        positive_tags = ['sensation']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 4800
        featurestep = 200
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'detectnewgatesensation':
        modelname = args[1]
        positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100', 'newgate', 'sensation']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2800
        featureend = 4400
        featurestep = 100
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'allgothic':
        modelname = args[1]
        positive_tags = ['stangothic', 'pbgothic', 'lochorror', 'locghost', 'chihorror']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'stangothic':
        modelname = args[1]
        positive_tags = ['stangothic']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'horror':
        modelname = args[1]
        positive_tags = ['chihorror']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'ghost':
        modelname = args[1]
        positive_tags = ['locghost']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'pbgothic':
        modelname = args[1]
        positive_tags = ['pbgothic']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'SFpreGernsback':
        modelname = args[1]
        positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 5400
        featurestep = 200
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags,negative_tags = ['random', 'grandom', 'chirandom'], excl_below = 1700, excl_above = 1925)

    elif args[1] == 'SFpostGernsback':
        modelname = args[1]
        positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 5400
        featurestep = 200
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags,negative_tags = ['random', 'grandom', 'chirandom'], excl_below = 1926, excl_above = 2000)

    elif args[1] == 'hardboiled':
        modelname = args[1]
        positive_tags = ['hardboiled']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'cozy':
        modelname = args[1]
        positive_tags = ['cozy']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'hardcozy':
        modelname = args[1]
        positive_tags = ['cozy', 'hardboiled']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2500
        featureend = 5000
        featurestep = 250
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'allSF':
        modelname = args[1]
        positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 6000
        featurestep = 200
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags)

    elif args[1] == 'SFutopia':
        modelname = args[1]
        positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi', 'chiutopia', 'chifantasy']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 6000
        featurestep = 200
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags, negative_tags = ['random', 'grandom', 'chirandom'], excl_below = 1700, excl_above = 2000)

    elif args[1] == 'makematrix':
        models = ['stangothic', 'horror', 'ghost', 'sensation', 'pbgothic']
        categories = ['stangothic', 'chihorror', 'locghost', 'sensation', 'pbgothic']
        books = ['JamesTurnOfScrew1898', 'StokerDracula1897', 'LovecraftCharlesDexter1927', '22708', '21362', 'PeakeTitusGroan1946', 'nyp.33433074931118', 'njp.32101068601341', 'mdp.39015004200997', 'njp.32101051650776']
        translations = {'JamesTurnOfScrew1898': 'James, Turn of the Screw', 'StokerDracula1897': 'Stoker, Dracula', 'LovecraftCharlesDexter1927': 'Lovecraft', '22708': 'King, Misery', '21362': 'Rice, Interview w/ Vampire', 'PeakeTitusGroan1946': 'Peake, Titus Groan', 'nyp.33433074931118': 'Brontë, Wuthering Heights', 'njp.32101068601341': 'Poe', 'mdp.39015004200997': 'Shelley, Frankenstein', 'njp.32101051650776': 'Radcliffe, Udolpho'}
        metadatapath = '/Users/tunder/Dropbox/fiction/meta/concatenatedmeta.csv'
        sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
        extension = '.tsv'

        frame = dict()
        bookcats = categories
        for k, v in translations.items():
            bookcats.append(v)

        for m in models:
            modelpath = '/Users/tunder/Dropbox/fiction/results/' + m + '.pkl'
            resultspath = '/Users/tunder/Dropbox/fiction/results/' + m + '.csv'
            allmodeled = train.apply_pickled_model(modelpath, sourcefolder, extension, metadatapath)
            incats = dict()
            for c in categories:
                incats[c] = []
            for i in allmodeled.index:
                g = allmodeled.loc[i, 'genretags']
                predict = allmodeled.loc[i, m]
                if math.isnan(predict):
                    continue

                for c in categories:
                    if c in g:
                        incats[c].append(predict)
                if i in books:
                    incats[translations[i]] = [predict]
            column = dict()
            for b in bookcats:
                column[b] = sum(incats[b]) / len(incats[b])

            frame[m] = column

        df = pd.DataFrame(frame)
        df.to_csv('thegothicmatrix.csv')

    elif args[1] == 'everythingmatrix':
        models = {'stangothic': "18c Gothic", 'horror': "20c horror", 'ghost': "ghost stories", 'sensation': 'sensation fiction', 'alldetectivepre1915': "detective pre-1915", 'alldetectivepost1914': "detective post-1914", 'SFpreGernsback': 'pre-Gernsback SF', 'SFpostGernsback': 'post-Gernsback SF', 'hardboiled': 'hardboiled detectives'}
        members = dict()
        for k, v in models.items():
            members[v] = set()
            resultspath = '/Users/tunder/Dropbox/fiction/results/' + k + '.csv'
            with open(resultspath, encoding = 'utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['realclass'] == '1':
                        members[v].add(row['volid'])

        books = []
        # translations = {'StokerDracula1897': 'Stoker, Dracula', 'mdp.39015004200997': 'Shelley, Frankenstein', 'mdp.39015038723360': 'Collins, Woman in White'}
        translations = {}
        metadatapath = '/Users/tunder/Dropbox/fiction/meta/concatenatedmeta.csv'
        sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
        extension = '.tsv'

        frame = dict()
        bookcats = []
        for k, v in models.items():
            bookcats.append(v)
        for k, v in translations.items():
            bookcats.append(v)

        for m, v in models.items():
            modelpath = '/Users/tunder/Dropbox/fiction/results/' + m + '.pkl'
            allmodeled = train.apply_pickled_model(modelpath, sourcefolder, extension, metadatapath)
            incats = dict()
            for k, v in models.items():
                incats[v] = []
            for i in allmodeled.index:

                predict = allmodeled.loc[i, m]
                if math.isnan(predict):
                    continue

                for k, v in models.items():
                    if i in members[v]:
                        incats[v].append(predict)
                if i in books:
                    incats[translations[i]] = [predict]
            column = dict()
            for b in bookcats:
                column[b] = sum(incats[b]) / len(incats[b])

            frame[m] = column

        df = pd.DataFrame(frame)
        df.to_csv('everythingmatrix.csv')


    elif args[1] == 'paceofchange':
        models = set()
        for center in range(1970, 1980, 10):
            floor = center - 30
            firstmodel = "SF" + str(floor) + "-" + str(center)
            if firstmodel not in models:
                models.add(firstmodel)
                positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi']
                c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
                featurestart = 3000
                featureend = 6000
                featurestep = 200
                genre_gridsearch(firstmodel, c_range, featurestart, featureend, featurestep, positive_tags, negative_tags = ['random', 'grandom', 'chirandom'], excl_below = floor, excl_above = (center - 1))
            ceiling = center + 30
            secondmodel = "SF" + str(center) + "-" + str(ceiling)
            models.add(secondmodel)
            positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi']
            c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
            featurestart = 3000
            featureend = 6000
            featurestep = 200
            genre_gridsearch(secondmodel, c_range, featurestart, featureend, featurestep, positive_tags, negative_tags = ['random', 'grandom', 'chirandom'], excl_below = center, excl_above = (ceiling-1))

            firstpath = '/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.pkl'
            secondpath = '/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.pkl'
            metadatapath = '/Users/tunder/Dropbox/fiction/meta/concatenatedmeta.csv'
            sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
            extension = '.tsv'
            firstonall = train.apply_pickled_model(firstpath, sourcefolder, extension, metadatapath)
            # firstonall.set_index('docid', inplace = True)
            secondonall = train.apply_pickled_model(secondpath, sourcefolder, extension, metadatapath)
            # secondonall.set_index('docid', inplace = True)
            firstonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.csv', index_col = 'volid')
            secondonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.csv', index_col = 'volid')

            firsttotal, firstright = comparison(firstonself, secondonall, secondmodel)
            secondtotal, secondright = comparison(secondonself, firstonall, firstmodel)

            print(firsttotal, firstright)
            print("Accuracy of " + secondmodel + " on volumes originally included in "+ firstmodel + ": " + str(firstright/firsttotal))
            print(secondtotal, secondright)
            print("Accuracy of " + firstmodel + " on volumes originally included in "+ secondmodel + ": " + str(secondright/secondtotal))
            totalaccuracy = (firstright + secondright) / (firsttotal + secondtotal)
            print(center)
            print("Total accuracy: ", str(totalaccuracy))

    elif args[1] == 'detectivepaceofchange':
        models = set()
        results = []
        for center in range(1960, 1980, 10):
            floor = center - 30
            firstmodel = "Detect" + str(floor) + "-" + str(center)
            if firstmodel not in models:
                models.add(firstmodel)
                positive_tags = ['locdetective', 'locdetmyst', 'chimyst', 'det100']
                c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
                featurestart = 3000
                featureend = 6000
                featurestep = 200
                genre_gridsearch(firstmodel, c_range, featurestart, featureend, featurestep, positive_tags, negative_tags = ['random', 'grandom', 'chirandom'], excl_below = floor, excl_above = (center - 1))
            ceiling = center + 30
            secondmodel = "Detect" + str(center) + "-" + str(ceiling)
            if secondmodel not in models:
                models.add(secondmodel)
                c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
                featurestart = 3000
                featureend = 6000
                featurestep = 200
                genre_gridsearch(secondmodel, c_range, featurestart, featureend, featurestep, positive_tags, negative_tags = ['random', 'grandom', 'chirandom'], excl_below = center, excl_above = (ceiling-1))

            firstpath = '/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.pkl'
            secondpath = '/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.pkl'
            metadatapath = '/Users/tunder/Dropbox/fiction/meta/concatenatedmeta.csv'
            sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
            extension = '.tsv'
            firstonall = train.apply_pickled_model(firstpath, sourcefolder, extension, metadatapath)
            # firstonall.set_index('docid', inplace = True)
            secondonall = train.apply_pickled_model(secondpath, sourcefolder, extension, metadatapath)
            # secondonall.set_index('docid', inplace = True)
            firstonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.csv', index_col = 'volid')
            secondonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.csv', index_col = 'volid')

            firsttotal, firstright = comparison(firstonself, secondonall, secondmodel)
            secondtotal, secondright = comparison(secondonself, firstonall, firstmodel)

            print(firsttotal, firstright)
            print("Accuracy of " + secondmodel + " on volumes originally included in "+ firstmodel + ": " + str(firstright/firsttotal))
            print(secondtotal, secondright)
            print("Accuracy of " + firstmodel + " on volumes originally included in "+ secondmodel + ": " + str(secondright/secondtotal))
            totalaccuracy = (firstright + secondright) / (firsttotal + secondtotal)
            print(center)
            print("Total accuracy: ", str(totalaccuracy))
            results.append(totalaccuracy)

    elif args[1] == 'mutualrecognition':
        detectiveresults = []
        for center in range(1890, 1980, 10):
            floor = center - 30
            firstmodel = "Detect" + str(floor) + "-" + str(center)
            ceiling = center + 30
            secondmodel = "Detect" + str(center) + "-" + str(ceiling)

            firstcsv = '/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.csv'
            secondcsv = '/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.csv'
            baseaccuracy = getacc([firstcsv, secondcsv])

            firstpath = '/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.pkl'
            secondpath = '/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.pkl'

            metadatapath = '/Users/tunder/Dropbox/fiction/meta/concatenatedmeta.csv'
            sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
            extension = '.tsv'
            firstonall = train.apply_pickled_model(firstpath, sourcefolder, extension, metadatapath)
            # firstonall.set_index('docid', inplace = True)
            secondonall = train.apply_pickled_model(secondpath, sourcefolder, extension, metadatapath)
            # secondonall.set_index('docid', inplace = True)
            firstonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.csv', index_col = 'volid')
            secondonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.csv', index_col = 'volid')

            firsttotal, firstright = comparison(firstonself, secondonall, secondmodel)
            secondtotal, secondright = comparison(secondonself, firstonall, firstmodel)

            print(firsttotal, firstright)
            print("Accuracy of " + secondmodel + " on volumes originally included in "+ firstmodel + ": " + str(firstright/firsttotal))
            print(secondtotal, secondright)
            print("Accuracy of " + firstmodel + " on volumes originally included in "+ secondmodel + ": " + str(secondright/secondtotal))
            totalaccuracy = (firstright + secondright) / (firsttotal + secondtotal)
            print(center)
            print("Total accuracy: ", str(totalaccuracy))
            print('Difference ' + str(totalaccuracy - baseaccuracy))
            detectiveresults.append(totalaccuracy - baseaccuracy)

        sfresults = []
        for center in range(1890, 1980, 10):
            floor = center - 30
            firstmodel = "SF" + str(floor) + "-" + str(center)
            ceiling = center + 30
            secondmodel = "SF" + str(center) + "-" + str(ceiling)

            firstcsv = '/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.csv'
            secondcsv = '/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.csv'
            baseaccuracy = getacc([firstcsv, secondcsv])

            firstpath = '/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.pkl'
            secondpath = '/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.pkl'

            metadatapath = '/Users/tunder/Dropbox/fiction/meta/concatenatedmeta.csv'
            sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
            extension = '.tsv'
            firstonall = train.apply_pickled_model(firstpath, sourcefolder, extension, metadatapath)
            # firstonall.set_index('docid', inplace = True)
            secondonall = train.apply_pickled_model(secondpath, sourcefolder, extension, metadatapath)
            # secondonall.set_index('docid', inplace = True)
            firstonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + firstmodel + '.csv', index_col = 'volid')
            secondonself = pd.read_csv('/Users/tunder/Dropbox/fiction/results/' + secondmodel + '.csv', index_col = 'volid')

            firsttotal, firstright = comparison(firstonself, secondonall, secondmodel)
            secondtotal, secondright = comparison(secondonself, firstonall, firstmodel)

            print(firsttotal, firstright)
            print("Accuracy of " + secondmodel + " on volumes originally included in "+ firstmodel + ": " + str(firstright/firsttotal))
            print(secondtotal, secondright)
            print("Accuracy of " + firstmodel + " on volumes originally included in "+ secondmodel + ": " + str(secondright/secondtotal))
            totalaccuracy = (firstright + secondright) / (firsttotal + secondtotal)
            print(center)
            print("Total accuracy: ", str(totalaccuracy))
            print('Difference ' + str(totalaccuracy - baseaccuracy))
            sfresults.append(totalaccuracy - baseaccuracy)

        print(detectiveresults)
        print(sfresults)

    elif args[1] == 'preGernsback50':
        modelname = args[1]
        positive_tags = ['locscifi', 'anatscifi', 'femscifi', 'chiscifi']
        c_range = [.0003, .001, .003, .006, .01, .03, .1, .3, 1, 8]
        featurestart = 2000
        featureend = 6200
        featurestep = 100
        genre_gridsearch(modelname, c_range, featurestart, featureend, featurestep, positive_tags,negative_tags = ['random', 'grandom', 'chirandom'], excl_below = 1850, excl_above = 1925)

