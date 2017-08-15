#!/usr/bin/env python3

# create_plot_data.py

# bootstrap resamples character probabilities
# for various categories and creates files
# that can be used to plot them diachronically

import csv
import numpy as np
import pandas as pd

def weighted_bootstrap_mean(probs, weights, indices, vectorlength):
    sample_indices = np.random.choice(indices, vectorlength, replace = True)
    prob_sample = probs[sample_indices]
    weight_sample = weights[sample_indices]
    sample_mean = np.average(prob_sample, weights = weight_sample)

    return sample_mean

def bootstrap_diff_weighted_means(fprobs, fweights, mprobs, mweights):
    '''
    Bootstrap resampling of a vector that is associated with a
    vector of weights. Returns lower bound, median, and upper
    bound for a 95% interval on 1000 bootstrap samples.
    '''

    assert len(fprobs) == len(fweights)
    femlength = len(fprobs)

    assert len(mprobs) == len(mweights)
    malelength = len(mprobs)

    meandiffs = []
    femindices = [x for x in range(femlength)]
    maleindices = [x for x in range(malelength)]

    for i in range(1000):
        femmean = weighted_bootstrap_mean(fprobs, fweights, femindices, femlength)
        malemean = weighted_bootstrap_mean(mprobs, mweights, maleindices, malelength)
        diff = femmean - malemean
        meandiffs.append(diff)

    low, middle, high = np.percentile(meandiffs, [2.5, 50, 97.5])

    return low, middle, high

def unweighted_bootstrap(probs):
    '''
    Bootstrap resampling of a vector. Returns lower bound,
    median, and upper bound for a 95% interval on 1000 bootstrap
    samples.
    '''

    vectorlength = len(probs)
    means = []

    for i in range(1000):
        prob_sample = np.random.choice(probs, vectorlength, replace = True)
        sample_mean = np.mean(prob_sample)
        means.append(sample_mean)

    low, middle, high = np.percentile(means, [2.5, 50, 97.5])

    return low, middle, high


gender_categories = {'f', 'm'}
probs = dict()
weights = dict()

for authgender in gender_categories:
    probs[authgender] = dict()
    weights[authgender] = dict()
    for chargender in gender_categories:
        probs[authgender][chargender] = dict()
        weights[authgender][chargender] = dict()
        for y in range(1785, 2008):
            probs[authgender][chargender][y] = []
            weights[authgender][chargender][y] = []

ctr = 0
with open('gender_probs.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        chargender = row['gender']
        docid = row['docid']
        authgender = row['authgender']

        if chargender not in gender_categories:
            continue
        if authgender not in gender_categories:
            continue

        year = int(row['pubdate'])
        if year < 1785 or year > 2007:
            continue

        probs[authgender][chargender][year].append(float(row['probability']))
        weights[authgender][chargender][year].append(float(row['numwords']))

        ctr += 1
        if ctr % 20000 == 1:
            print(ctr)

outrows = []

for ag in gender_categories:
    for y in range(1790, 2008):
        print(ag, y)
        femprobs = np.array([])
        femweights = np.array([])
        maleprobs = np.array([])
        maleweights = np.array([])
        for y1 in range(y - 1, y + 2):
            if y1 > 2007:
                break
            if y1 not in weights[ag]['f']:
                print('skipping ', y1)
                continue
            femprobs = np.append(femprobs, np.array(probs[ag]['f'][y1]))
            femweights = np.append(femweights, np.array(weights[ag]['f'][y1]))
            maleprobs = np.append(maleprobs, np.array(probs[ag]['m'][y1]))
            maleweights = np.append(maleweights, np.array(weights[ag]['m'][y1]))

        low, middle, high = bootstrap_diff_weighted_means(femprobs, femweights, maleprobs, maleweights)
        out = dict()
        out['authgender'] = ag
        out['year'] = y
        out['median'] = middle
        out['upper'] = high
        out['lower'] = low
        outrows.append(out)

fieldnames = ['authgender', 'year', 'lower', 'median', 'upper']

with open('..dataforR/differentiation_plot.csv', mode = 'w', encoding = 'utf-8') as f:
    scribe = csv.DictWriter(f, fieldnames = fieldnames)
    scribe.writeheader()
    for row in outrows:
        scribe.writerow(row)






