#!/usr/bin/env python3

# apply_model_to_characters.py

# There was already an apply_pickled_model function in
# versatile_trainer, but it was designed to work with
# folders of files, and this will be easier if we use
# the tabular data.

# USAGE:

# python3 apply_model_to_characters.py modeldir datadir outpath

# where
# modeldir       is a directory home to decade models from 1790 through 2000
# datafile       the character_table to be processed
# outpath        is the name of the file to be written; for me,
#                gender_probs_for_diff.tsv

# what I actually did:

# 1) python apply_model_to_characters.py ../models/ ../data/character_table_pre1850.tsv ../gender_probs_for_diff.tsv
# 2) python apply_model_to_characters.py modelsused/fifty1850-1899.pkl ../data/character_table_1850to99.tsv ../gender_probs_for_diff.tsv
# 3) python apply_model_to_characters.py modelsused/fifty1900-1949.pkl ../data/character_table_1900to1949.tsv ../gender_probs_for_diff.tsv
# 4) python apply_model_to_characters.py modelsused/fiftypost1950.pkl ../data/character_table_post1950.tsv ../gender_probs_for_diff.tsv

import numpy as np
import pandas as pd
import csv, os, random, sys, datetime, pickle
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

csv.field_size_limit(sys.maxsize)

forbidden = {'he', 'she', 'her', 'him', 'manhood', 'womanhood', 'boyhood', 'girlhood', 'husband', 'wife', 'lordship', 'ladyship', 'man', 'woman', 'mistress', 'daughter', 'son', 'girl', 'boy', 'bride', 'fiancé', 'fiancée', 'brother', 'sister', 'lady', 'gentleman'}

def get_model(amodelpath):
    with open(amodelpath, 'rb') as input:
        modeldict = pickle.load(input)

    return modeldict

def apply_pickled_model(modeldict, masterdata):
    '''
    Loads a model pickled by the export_model() function above, and applies it to
    a group of texts. Returns a pandas dataframe with a new column for the
    predictions created by this model. The model name becomes the column name.
    This allows us to build up a metadata file with columns for the predictions
    made by multiple models.
    '''
    model = modeldict['itself']
    scaler = modeldict['scaler']

    standarddata = scaler.transform(masterdata)
    probabilities = [x[1] for x in model.predict_proba(standarddata)]

    return probabilities

def write_a_chunk(chunk, metarows, modeldict, outpath, no_header_yet):
    fieldnames = ['docid', 'charid', 'gender', 'authgender', 'pubdate', 'numwords', 'probability']
    masterdata = pd.DataFrame(chunk)
    probabilities = apply_pickled_model(modeldict, masterdata)

    with open(outpath, mode = 'a', encoding = 'utf-8') as f2:
        writer = csv.DictWriter(f2, fieldnames = fieldnames, delimiter = '\t')
        if no_header_yet:
            writer.writeheader()
            no_header_yet = False
        for row, prob in zip(metarows, probabilities):
            row['probability'] = prob
            writer.writerow(row)

    return no_header_yet

def cycle_through(inpath, allmodels, outpath, no_header_yet):

    global forbidden

    metadata = pd.read_csv('../metadata/filtered_fiction_plus_18c.tsv', sep ='\t')
    alldocs = set(metadata.docid)
    doc2authgender = pd.Series(metadata.authgender.values, index = metadata.docid).to_dict()

    ctr = 0

    missing = 0

    with open(inpath, encoding = 'utf-8') as f1:
        reader = csv.DictReader(f1, delimiter = '\t')

        databydecade = dict()
        metadatabydecade = dict()
        thischunk = 0

        for row in reader:
            newrow = dict()
            newrow['docid'] = row['docid']
            newrow['charid'] = row['charid']
            newrow['gender'] = row['gender']
            newrow['pubdate'] = row['pubdate']
            decade = 10 * (int(row['pubdate']) // 10)
            if decade < 1790:
                decade = 1790

            if decade not in allmodels:
                continue
            else:
                vocabmap = allmodels[decade]['vocabmap']

            words = row['words']

            words = row['words'].split(' ')

            if len(words) < 5:
                continue
            # we're ignoring minor characters

            newrow['numwords'] = len(words)
            if newrow['docid'] in alldocs:
                newrow['authgender'] = doc2authgender[newrow['docid']]
            else:
                newrow['authgender'] = 'u'
                missing += 1

            wordctr = Counter()
            wordtotal = 0
            for w in words:
                if w not in forbidden and not w.startswith('said-'):
                    wordctr[w] += 1
                    wordtotal += 1

            if wordtotal < 5:
                continue

            wordvec = np.zeros(numwords)
            for w, count in wordctr.items():
                if w in vocabmap:
                    idx = vocabmap[w]
                    wordvec[idx] = count / wordtotal

            if decade not in databydecade:
                databydecade[decade] = []
                metadatabydecade[decade] = []

            databydecade[decade].append(wordvec)
            metadatabydecade[decade].append(newrow)
            thischunk += 1

            if thischunk > 50000:
                for dec, data in databydecade.items():
                    meta = metadatabydecade[dec]
                    no_header_yet = write_a_chunk(data, meta, allmodels[dec], outpath, no_header_yet)
                databydecade = dict()
                metadatabydecade = dict()
                thischunk = 0
                print('writing ' + str(ctr))
                ctr += 1

        # catch the last chunk
        if thischunk > 0:
            for dec, data in databydecade.items():
                meta = metadatabydecade[dec]
                no_header_yet = write_a_chunk(data, meta, allmodels[dec], outpath, no_header_yet)
            databydecade = dict()
            metadatabydecade = dict()
            thischunk = 0
            print('writing ' + str(ctr))
            ctr += 1
    print(missing)
    return no_header_yet

# MAIN

args = sys.argv

modeldir = args[1]
sourcedata = args[2]
outpath = args[3]

if os.path.exists(outpath):
    no_header_yet = False
else:
    no_header_yet = True

allmodels = dict()

for d in range(1790, 2010, 10):
    modelpath = os.path.join(modeldir, 'thirty' + str(d) + '.pkl')
    modeldict = get_model(modelpath)
    vocabulary = modeldict['vocabulary']
    numwords = len(vocabulary)
    vocabmap = dict()
    for i, w in enumerate(vocabulary):
        vocabmap[w] = i
    modeldict['vocabmap'] = vocabmap
    allmodels[d] = modeldict

# process character table
no_header_yet = cycle_through(sourcedata, allmodels, outpath, no_header_yet)


