#!/usr/bin/env python3

# balance_by_gender.py

import csv, os, sys, pickle, math
import pandas as pd

def make_decade(year):
    year = int(year)
    decade = 10 * (year // 10)
    return decade


def do_balancing(adataframe, acolumn, startdate, endate, elitetag, randomtag):
    subframes = []
    if acolumn == 'gender':
        for i in range(startdate, endate, 10):
            thisdecade = adataframe[adataframe.decade == i]
            elitemen = thisdecade[(thisdecade.gender == 'm') & (thisdecade.tags == elitetag)]
            elitewomen = thisdecade[(thisdecade.gender == 'f') & (thisdecade.tags == elitetag)]
            vulgarmen = thisdecade[(thisdecade.gender == 'm') & (thisdecade.tags == randomtag)]
            vulgarwomen = thisdecade[(thisdecade.gender == 'f') & (thisdecade.tags == randomtag)]
            mincount = min(len(elitewomen), len(elitemen), len(vulgarwomen), len(vulgarmen))
            if mincount > 0:
                subframes.append(elitemen.sample(n = mincount))
                subframes.append(elitewomen.sample(n = mincount))
                subframes.append(vulgarwomen.sample(n = mincount))
                subframes.append(vulgarmen.sample(n = mincount))
    else:
        for i in range(startdate, endate, 10):
            thisdecade = adataframe[adataframe.decade == i]
            elitebrits = thisdecade[(thisdecade.nationality == 'uk') & (thisdecade.tags == elitetag)]
            eliteyanks = thisdecade[(thisdecade.nationality == 'us') & (thisdecade.tags == elitetag)]
            vulgarbrits = thisdecade[(thisdecade.nationality == 'uk') & (thisdecade.tags == randomtag)]
            vulgaryanks = thisdecade[(thisdecade.nationality == 'us') & (thisdecade.tags == randomtag)]
            mincount = min(len(elitebrits), len(eliteyanks), len(vulgarbrits), len(vulgaryanks))
            if mincount > 0:
                subframes.append(elitebrits.sample(n = mincount))
                subframes.append(eliteyanks.sample(n = mincount))
                subframes.append(vulgarbrits.sample(n = mincount))
                subframes.append(vulgaryanks.sample(n = mincount))

    return pd.concat(subframes)

existingframe = pd.read_csv('../metadata/prestigeficmeta.csv')
existingframe['gender'] = existingframe.gender.str.strip()
decmap = dict()
for i in range(1800, 2000):
    decmap[i] = make_decade(i)
existingframe['decade'] = existingframe.earliestdate.map(decmap)
newframe = do_balancing(existingframe, 'gender', 1850, 1950, 'elite', 'vulgar')
newframe.to_csv('../metadata/genderbalancedfiction.csv', index = False)

existingframe = pd.read_csv('../metadata/prestigeficmeta.csv')
existingframe['nationality'] = existingframe.nationality.str.strip()
existingframe['decade'] = existingframe.earliestdate.map(decmap)
newframe = do_balancing(existingframe, 'nationality', 1850, 1950, 'elite', 'vulgar')
newframe.to_csv('../metadata/nationbalancedfiction.csv', index = False)

existingframe = pd.read_csv('../metadata/prestigepoemeta.csv')
existingframe['nationality'] = existingframe.nationality.str.strip()
existingframe['decade'] = existingframe.earliestdate.map(decmap)
newframe = do_balancing(existingframe, 'nationality', 1820, 1920, 'reviewed', 'random')
newframe.to_csv('../metadata/nationbalancedpoetry.csv', index = False)

newframe = do_balancing(existingframe, 'gender', 1820, 1920, 'reviewed', 'random')
newframe.to_csv('../metadata/genderbalancedpoetry.csv', index = False)

