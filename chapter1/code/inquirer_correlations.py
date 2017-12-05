#!/usr/bin/env python3

import csv, os, sys
from collections import Counter

# import utils
currentdir = os.path.dirname(__file__)
libpath = os.path.join(currentdir, '../../lib')
sys.path.append(libpath)

import SonicScrewdriver as utils
import FileCabinet as filecab
import numpy as np
from scipy.stats import pearsonr

# start by loading the dictionary

dictionary = set()

with open('../lexicons/MainDictionary.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        word = row[0]
        count = int(row[2])
        if count < 10000:
            continue
        else:
            dictionary.add(word)

colors = set()
onesense = dict()
inquirer = dict()

suffixes = dict()
suffixes['verb'] = ['s', 'es', 'ed', 'd', 'ing']
suffixes['noun'] = ['s', 'es']

with open('../lexicons/inquirerbasic.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames[2:-2]
    for field in fields:
        inquirer[field] = set()
        onesense[field] = set()

    for row in reader:
        term = row['Entry']

        if '#' in term:
            parts = term.split('#')
            word = parts[0].lower()
            sense = int(parts[1].strip('_ '))
            partialsense = True
        else:
            word = term.lower()
            sense = 0
            partialsense = False

        if sense > 1:
            continue
            # we're ignoring uncommon senses

        pos = row['Othtags']
        if 'Noun' in pos:
            pos = 'noun'
        elif 'SUPV' in pos:
            pos = 'verb'

        forms = {word}
        if pos == 'noun' or pos == 'verb':
            for suffix in suffixes[pos]:
                if word + suffix in dictionary:
                    forms.add(word + suffix)
                if pos == 'verb' and word.rstrip('e') + suffix in dictionary:
                    forms.add(word.rstrip('e') + suffix)

        for form in forms:
            for field in fields:
                if len(row[field]) > 1:
                    inquirer[field].add(form)

print('inquirer loaded')
sourcedir = '../sourcefiles/'

docs = []
logistic = []
dates = []

with open('../plotdata/allsubset2.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        genre = row['realclass']
        docid = row['volid']
        if not os.path.exists(sourcedir + docid + '.tsv'):
            continue
        docs.append(row['volid'])
        logistic.append(float(row['logistic']))
        dates.append(float(row['dateused']))

logistic = np.array(logistic)
dates = np.array(dates)

numdocs = len(docs)

categories = dict()
for field in fields:
    categories[field] = np.zeros(numdocs)

wordcounts = filecab.get_wordcounts(sourcedir, '.tsv', docs)

for i, doc in enumerate(docs):
    ctcat = Counter()
    allcats = 0
    for word, count in wordcounts[doc].items():
        allcats += count
        for field in fields:
            if word in inquirer[field]:
                ctcat[field] += count
    for field in fields:
        categories[field][i] = ctcat[field] / (allcats + 1)

logresults = []
dateresults = []

# I compute correlations with date but don't print them;
# this is vestigial from EDA.

for field in fields:
    l = pearsonr(logistic, categories[field])[0]
    logresults.append((l, field))
    d = pearsonr(dates, categories[field])[0]
    dateresults.append((d, field))

logresults.sort()
dateresults.sort()

# Now we load a dictionary that translates some of the short, opaque
# terms used in the General Inquirer into phrases that are a little
# more illuminating. Are these "translations" debatable? Yes.
# But I have tried to base them on the descriptions at
# http://www.wjh.harvard.edu/~inquirer/homecat.htm

short2long = dict()
with open('../lexicons/long_inquirer_names.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        short2long[row['short_name']] = row['long_name']

print('Printing the correlations of General Inquirer categories')
print('with the predicted probabilities of being fiction in allsubset2.csv:')
print()
for prob, n in logresults:
    if n in short2long:
        n = short2long[n]
    print(n+ '\t' + str(prob))







