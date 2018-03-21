#!/usr/bin/env python3

# apply_surprise_metric.py

import sys, os, csv, random
import numpy as np
from collections import Counter

date = sys.argv[1]
novelname = sys.argv[2]

# USAGE:
# python3 apply_normalized_surprise_metric.py 1940 leguinlefthand.txt

# The program looks for a surprise-metric file in the surprisemetrics subfolder,
# using "date" (above) to generate the name of the file.

# It also looks for "novelname" in a sibling folder called "rawtexts."

# Then it applies the surprise-metric to the novel, after first breaking
# the novel into ~250-word chunks. It uppercases the 2000 words that have the
# biggest positive effect on surprise (i.e., words that are more likely
# in the later of the two periods that were contrasted to create the
# the surprise metric).


def onlyalpha(word):
    only = ''
    for char in word:
        if char.isalpha():
            only = only + char
    return only

inpath = '../rawtexts/' + novelname

with open(inpath, encoding = 'utf-8') as f:
    lines = f.readlines()

coefs = dict()
with open('surprisemetrics/surprise_in_' + str(date) + '.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        coefs[row['word']] = float(row['coef'])

pages = []
ctr = 0
for l in lines:
    if l.startswith('“Stranger In'):
        continue

    if ctr == 0:
        page = []
    page.append(l)
    wordct = len(l.split())
    ctr += wordct
    if ctr > 250:
        pages.append(page)
        ctr = 0

# first let's get total wordcounts
wordcounts = Counter()

for p in pages:

    for l in p:
        l = l.replace('-', ' ')
        l = l.replace('—', ' ')
        l = l.replace(',', ' ')
        words = l.split()
        for origw in words:
            w = onlyalpha(origw.lower())
            if w in coefs:
                wordcounts[w] += 1

significant = []

for word, coef in coefs.items():
    if coef > 0:
        significant.append((coef, word))

significant.sort(reverse = True)

significant = set([x[1] for x in significant[0: 2500]])

pageprobs = []
transpages = []

for p in pages:
    wordcounts = Counter()
    total = 0

    translated = []

    for l in p:
        l = l.replace('-', ' ')
        l = l.replace('—', ' ')
        l = l.replace(',', ' ')
        words = l.split()
        for origw in words:
            w = onlyalpha(origw.lower())
            if w in coefs:
                wordcounts[w] += 1
                if w in significant:
                    translated.append(origw.upper())
                else:
                    translated.append(origw)
            else:
                translated.append(origw)

            total += 1

    prob = 0

    for word, count in wordcounts.items():
        freq = count / total
        prob += (freq * coefs[word])

    pageprobs.append(prob)
    transpages.append(' '.join(translated))

tuplepages = [x for x in zip(pageprobs, transpages)]

tuplepages.sort(reverse = True)

with open('surprise_' + novelname, mode = 'w', encoding = 'utf-8') as f:
    for p, t in tuplepages:
        f.write('SURPRISE: ' + str(p) + '\n')
        f.write('\n')
        f.write(t)
        f.write('\n\n')













