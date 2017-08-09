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

stanford = set()

with open('../lexicons/stanford.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['class'] == 'hard':
            stanford.add(row['word'])

sourcedir = '../sourcefiles/'

pairedpaths = filecab.get_pairedpaths(sourcedir, '.tsv')

docids = [x[0] for x in pairedpaths]

wordcounts = filecab.get_wordcounts(sourcedir, '.tsv', docids)

metapath = '../metadata/allgenremeta.csv'

genredict = dict()
datedict = dict()
with open(metapath, encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date = int(row['firstpub'])
        genre = row['genretags']
        docid = row['docid']
        if date not in datedict:
            datedict[date] = []
        datedict[date].append(docid)
        genredict[docid] = genre

possible_genres = {'poe', 'fic', 'bio'}
allcounts = dict()
hardseedcounts = dict()
for genre in possible_genres:
    allcounts[genre] = Counter()
    hardseedcounts[genre] = Counter()

for i in range(1700,2000):
    if i in datedict:
        candidates = datedict[i]
        for anid in candidates:
            genre = genredict[anid]
            if anid not in wordcounts:
                print('error')
                continue
            else:
                for word, count in wordcounts[anid].items():
                    allcounts[genre][i] += count
                    if word in stanford:
                        hardseedcounts[genre][i] += count

with open('plotdata/hardaverages.csv', mode = 'w', encoding = 'utf-8') as f:
    f.write('genre,year,hardpct\n')
    for genre in possible_genres:
        for i in range(1700,2000):
            if i in allcounts[genre]:
                pct = hardseedcounts[genre][i] / (allcounts[genre][i] + 1)
                f.write(genre + ',' + str(i) + ',' + str(pct) + '\n')




