#!/usr/bin/env python3

import csv, os, sys
from collections import Counter

# import utils
currentdir = os.path.dirname(__file__)
libpath = os.path.join(currentdir, '../../lib')
sys.path.append(libpath)

import SonicScrewdriver as utils
import FileCabinet as filecab

# start by loading the hard seeds

colors = set()

with open('../lexicons/colors.txt', encoding = 'utf-8') as f:
    for line in f:
        colors.add(line.strip())

logistic = dict()
realclass = dict()
titles = dict()
dates = dict()

with open('../metadata/prestigeset.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        logistic[row['volid']] = float(row['logistic'])
        realclass[row['volid']] = row['prestige']
        titles[row['volid']] = row['title']
        dates[row['volid']] = int(row['dateused'])

sourcedir = '../sourcefiles/'
documents = filecab.get_wordcounts(sourcedir, '.tsv', set(logistic))

outrows = []

for docid, doc in documents.items():
    if docid not in logistic:
        continue
    else:
        allwords = 1
        colorct = 0

        for word, count in doc.items():
            allwords += count
            if word in colors:
                colorct += count

        outline = [docid, realclass[docid], logistic[docid], (colorct/allwords), dates[docid], titles[docid]]
        outrows.append(outline)

fields = ['docid', 'class', 'logistic', 'colors', 'date', 'title']
with open('../plotdata/colorfic.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    for row in outrows:
        writer.writerow(row)





