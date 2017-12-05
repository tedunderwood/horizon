#!/usr/bin/env python3

import csv, os, sys
from collections import Counter

# filecabinet

abcdef = 'abcdefghijklmnopqrstuvwxyz., ABCDEFGHIJKLMNOPQRSTUVWXYZ()?'

def get_wordcounts(directoryname, extension, set2get):
    '''
    Slurps up a whole directory of tsv files containing
    words paired with counts. Returns them as a dictionary
    where keys are document IDs and values are Counters()
    holding the wordcounts. Assumes that the filename will
    be document ID + extension.
    '''

    documents = dict()

    filelist = os.listdir(directoryname)
    pathlist = [os.path.join(directoryname, x) for x in filelist if x.endswith(extension)]
    docidlist = [x.replace(extension, '') for x in filelist if x.endswith(extension)]

    for docid, path in zip(docidlist, pathlist):

        if docid not in set2get:
            continue

        counts = Counter()
        with open(path, encoding = 'utf-8') as f:
            for line in f:
                fields = line.strip().split()

                if len(fields) < 2 or len(fields) > 2:
                    continue

                else:
                    word = fields[0]
                    count = int(fields[1])
                    counts[word] += count

        documents[docid] = counts

    return documents

def get_wordfreqs(directoryname, extension, set2get):
    '''
    Slurps up a whole directory of tsv files containing
    words paired with frequencies. Returns them as a dictionary
    where keys are document IDs and values are dictionaries
    holding the frequencies. Assumes that the filename will
    be document ID + extension.

    Also assumes first line is a header.
    '''

    documents = dict()

    filelist = os.listdir(directoryname)
    pathlist = [os.path.join(directoryname, x) for x in filelist if x.endswith(extension)]
    docidlist = [x.replace(extension, '') for x in filelist if x.endswith(extension)]

    for docid, path in zip(docidlist, pathlist):

        if docid not in set2get:
            continue

        counts = dict()
        errors = 0
        with open(path, encoding = 'utf-8') as f:
            for idx, line in enumerate(f):
                fields = line.strip().split()

                if len(fields) < 2 or len(fields) > 2:
                    continue
                else:
                    word = fields[0]
                    try:
                        count = float(fields[1])
                        counts[word] = count
                    except:
                        errors += 1

        documents[docid] = counts
        if errors > 1:
            print('More than one error in ' + docid)
            # we assume one error is just the header line

    return documents

def get_pairedpaths(directoryname, extension):
    filelist = os.listdir(directoryname)
    pathlist = [os.path.join(directoryname, x) for x in filelist if x.endswith(extension)]
    docidlist = [x.replace(extension, '') for x in filelist if x.endswith(extension)]

    return zip(docidlist, pathlist)

def clean_number(astring):
    global abcdef

    if len(astring) < 1:
        return 0

    astring = astring.strip(abcdef)
    if astring.isdigit():
        return int(astring)
    else:
        return 0

def parse_authordate(authdate):
    '''
    Parses an authordate field from MARC. Note that this function is
    strongly shaped by an assumption that I'm only interested in dates from
    the last millenium or so. Thus zero and negative numbers work as error
    indicators.
    '''

    authdate = authdate.strip()

    if len(authdate) < 1:
        return 0, 0
    elif 'B.C' in authdate or 'BC' in authdate:
        return -1, -1
    elif '-' in authdate:
        fields = authdate.split('-')
        if len(fields) < 2:
            return 0, 0
        else:
            birth = clean_number(fields[0])
            death = clean_number(fields[1])

            if birth == 0 and death > 0:
                # this is a death date without birth date
                # problem: we usually need the birth date
                # solution: egregious guessing
                birth = death - 50
            elif death == 0 and birth > 0:
                death = birth + 50

            if death < birth:
                return -2, -2
                # we screwed that one up

            return birth, death

    elif authdate.startswith('b.'):
        # born
        birth = clean_number(authdate)
        if birth > 0:
            death = birth + 50
        else:
            death = 0

        return birth, death

    elif authdate.startswith('d.'):
        # died
        death = clean_number(authdate)
        if death > 0:
            birth = death - 50
        else:
            birth = 0

        return birth, death

    elif authdate.startswith('fl.'):
        # floruit
        floruit = clean_number(authdate)
        birth = floruit - 25
        death = floruit + 25
        return birth, death

    elif 'cent' in authdate:
        century = clean_number(authdate)
        if century > 0 and century < 20:
            birth = century * 100
            death = century * 100 + 50
            return birth, death
        else:
            return 0, 0
    else:
        return -2, -2
        # we failed to parse this one

def flipname(aname):
    '''
    Parenthetical aliases should follow initials, not precede them.
    '''

    if not aname.startswith('('):
        return aname

    if not '),' in aname:
        return aname

    twoparts = aname.split('),')
    if len(twoparts) > 2 or len(twoparts) < 2:
        return aname
    else:
        aname = twoparts[1].strip(', ') + ' ' + twoparts[0] + '),'
        return aname












