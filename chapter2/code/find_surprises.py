#!/usr/bin/env python3

# find_surprises.py

# The intuition here is that we're going to look at models'
# predictions about the future and try to figure out where
# they go wrong. What are the surprises in the period
# 1930-70 that make it difficult to predict?

# We could do the reverse as well, if we had time.

import csv, os, sys, pickle, math
import pandas as pd

def futurepredict():
    sfresults = []
        for iteration in range(5):
            for center in range(1890, 1980, 10):
                floor = center - 30
                firstmodel = "SF" + str(iteration) + '-' + str(floor) + "-" + str(center)
                ceiling = center + 30
                secondmodel = "SF" + str(iteration) + '-' +str(center) + "-" + str(ceiling)

                firstcsv = '../modeloutput/' + firstmodel + '.csv'
                secondcsv = '../modeloutput/' + secondmodel + '.csv'
                baseaccuracy = getacc([firstcsv, secondcsv])

                firstpath = '../modeloutput/' + firstmodel + '.pkl'
                secondpath = '../modeloutput/' + secondmodel + '.pkl'

                metadatapath = '../metadata/SFsample' + str(iteration) + '.csv'
                sourcefolder = '/Users/tunder/Dropbox/fiction/newtsvs'
                extension = '.tsv'
                firstonall = train.apply_pickled_model(firstpath, sourcefolder, extension, metadatapath)
                # firstonall.set_index('docid', inplace = True)
                secondonall = train.apply_pickled_model(secondpath, sourcefolder, extension, metadatapath)
                # secondonall.set_index('docid', inplace = True)
                firstonself = pd.read_csv('../modeloutput/' + firstmodel + '.csv', index_col = 'volid')
                secondonself = pd.read_csv('../modeloutput/' + secondmodel + '.csv', index_col = 'volid')

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
                outline = str(iteration) + '\t' + str(center) + '\t' + str(baseaccuracy) + '\t' + str(totalaccuracy) + '\t' + str(baseaccuracy - totalaccuracy) + '\n'
                sfresults.append(outline)

