#!/usr/bin/env python3

# find_surprises.py

# The intuition here is that we're going to look at models'
# predictions about the future and try to figure out where
# they go wrong. What are the surprises in the period
# 1930-70 that make it difficult to predict?

# We could do the reverse as well, if we had time.

import csv, os, sys, pickle, math
import pandas as pd

# add the path to the logistic folder at a higher
# level of the repo
sys.path.append('../../logistic/')
import versatiletrainer as train

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


def futurepredict():
    differences = dict()
    dates = dict()
    authors = dict()
    titles = dict()
    genders = dict()

    for iteration in range(5):
        print('ITERATION: ' + str(iteration))
        for center in range(1930, 1970, 10):
            print('CENTER: ' + str(center))
            floor = center - 30
            firstmodel = "SF" + str(iteration) + '-' + str(floor) + "-" + str(center)
            ceiling = center + 30
            secondmodel = "SF" + str(iteration) + '-' +str(center) + "-" + str(ceiling)

            firstpath = '../modeloutput/' + firstmodel + '.pkl'

            metadatapath = '../metadata/concatenatedmeta.csv'
            sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
            extension = '.tsv'
            firstonall = train.apply_pickled_model(firstpath, sourcefolder, extension, metadatapath)

            secondonself = pd.read_csv('../modeloutput/' + secondmodel + '.csv', index_col = 'volid')

            for docid in secondonself.index:
                # print(docid, firstmodel)
                date = secondonself.loc[docid, 'dateused']
                realclass = int(secondonself.loc[docid, 'realclass'])
                selfprediction = secondonself.loc[docid, 'logistic']

                if date < 1930 or date > 1976:
                    continue

                if realclass == 0:
                    continue

                try:
                    predictionfrompast = firstonall.loc[docid, firstmodel]
                    # this gets the prediction about this book made by a model in the past
                except:
                    try:
                        predictionfrompast = firstonall.loc[str(docid), firstmodel]
                    except:
                        print(docid, firstmodel, secondonself.loc[docid, 'title'])
                        continue

                diff = predictionfrompast - selfprediction

                if docid not in differences:
                    differences[docid] = []

                differences[docid].append(diff)
                dates[docid] = date
                authors[docid] = secondonself.loc[docid, 'author']
                titles[docid] = secondonself.loc[docid, 'title']
                genders[docid] = secondonself.loc[docid, 'gender']

    with open('../plotdata/sfsurprises.tsv', mode = 'w', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, delimiter = '\t', fieldnames = ['docid', 'date', 'gender', 'diff', 'author', 'title'])
        writer.writeheader()
        for docid, date in dates.items():
            o = dict()
            o['docid'] = docid
            o['date'] = date
            o['diff'] = sum(differences[docid]) / len(differences[docid])
            o['author'] = authors[docid]
            o['title'] = titles[docid]
            o['gender'] = genders[docid]
            writer.writerow(o)


futurepredict()
