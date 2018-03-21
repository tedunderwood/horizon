#!/usr/bin/env python3

# main_experiment.py

import sys, os, csv, random
import numpy as np
import pandas as pd

date = int(sys.argv[1])

def addtodict(adict, afilename):
    path = '../modeloutput/' + afilename + '.coefs.csv'
    with open(path, encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            word = row[0]
            if len(word) < 1 or not word[0].isalpha():
                continue
                # we're just using alphabetic words for this

            coef = float(row[2])
            # note that a great deal depends on the difference between
            # row[1] (the unadjusted coefficient) and row[2] (the
            # coefficient divided by the .variance of the scaler for
            # this word, aka "how much a single instance of the word
            # moves the needle.")

            if word in adict:
                adict[word].append(coef)
            else:
                adict[word] = [coef]

    return adict

periods = [(1870, 1899), (1900, 1929), (1930, 1959), (1960, 1989), (1990, 2010), (1880, 1909), (1910, 1939), (1940, 1969), (1970, 1999), (1890, 1919), (1920, 1949), (1950, 1979), (1980, 2009)]

# identify the periods at issue

for floor, ceiling in periods:
    if ceiling+ 1 == date:
        f1, c1 = floor, ceiling
    if floor == date:
        f2, c2 = floor, ceiling

new = dict()
old = dict()

for i in range(5):
    for j in range(5):
        for part in [1, 2]:

            name1 = 'rccsf'+ str(f1) + '_' + str(c1) + '_' + str(i) + '_' + str(part)
            name2 = 'rccsf'+ str(f2) + '_' + str(c2) + '_' + str(j) + '_' + str(part)

            addtodict(old, name1)
            addtodict(new, name2)

allwords = set([x for x in old.keys()]).union(set([x for x in new.keys()]))

with open('crudemetrics/surprise_in_' + str(date) + '.csv', mode = 'w', encoding = 'utf-8') as f:
    scribe = csv.DictWriter(f, fieldnames = ['word', 'coef'])
    scribe.writeheader()

    for w in allwords:
        if w in old:
            oldcoef = sum(old[w]) / len(old[w])
        else:
            oldcoef = 0

        if w in new:
            newcoef = sum(new[w]) / len(new[w])
        else:
            newcoef = 0

        o = dict()
        o['word'] = w
        o['coef'] = (newcoef - oldcoef) / 1000000
        scribe.writerow(o)



