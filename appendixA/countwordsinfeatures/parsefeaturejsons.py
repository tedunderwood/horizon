#!/usr/bin/env python3

# parsefeaturejsons.py

# classes and functions that can unpack the extracted feature files
# created by HTRC, and convert them into a .csv that is easier to
# manipulate

import csv, os, sys, bz2, random, json
from collections import Counter

import numpy as np
import pandas as pd

# import utils
currentdir = os.path.dirname(__file__)
libpath = os.path.join(currentdir, '../lib')
sys.path.append(libpath)

import SonicScrewdriver as utils

abspath = os.path.abspath(__file__)
thisdirectory = os.path.dirname(abspath)
namepath = os.path.join(thisdirectory, 'PersonalNames.txt')
placepath = os.path.join(thisdirectory, 'PlaceNames.txt')
romanpath = os.path.join(thisdirectory, 'RomanNumerals.txt')

with open(namepath, encoding = 'utf-8') as f:
    personalnames = set([x.strip().lower() for x in f.readlines()])

with open(placepath, encoding = 'utf-8') as f:
    placenames = set([x.strip().lower() for x in f.readlines()])

with open(romanpath, encoding = 'utf-8') as f:
    romannumerals = set([x.strip().lower() for x in f.readlines()])

daysoftheweek = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
monthsoftheyear = {'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'}

# This is a little bit of a cheat, because it means we're not inferring everything
# empirically from evidence, but this is the product of a lot of previous experience,
# and hard-coding it here makes it possible to do a nice normalization at the page
# level.
ficwords = {'me', 'my', 'i', 'you', 'your', 'she', 'her', 'hers', 'he', 'him', 'his', 'the', 'said'}

def normalize_token(token):
    ''' Normalizes a token by lowercasing it and by bundling
    certain categories together. The lists of personal and place names
    are never going to be all-inclusive; you have to be aware of that,
    and deactivate this in corpora where it could pose a problem.
    '''

    global personalnames, placenames, daysoftheweek, monthsoftheyear

    token = token.lower()
    if len(token) < 1:
        return token
    elif token[0].isdigit() and token[-1].isdigit():
        return "#arabicnumeral"
    elif token in daysoftheweek:
        return "#dayoftheweek"
    elif token in monthsoftheyear:
        return "#monthoftheyear"
    elif token in personalnames:
        return "#personalname"
    elif token in placenames:
        return "#placename"
    else:
        return token

def normalize_token_for_page(token):
    ''' Normalizes a token by lowercasing it and by bundling
    certain categories together. Differs from the previous
    function in adding roman numerals.
    '''

    global personalnames, placenames, daysoftheweek, monthsoftheyear, romannumerals

    if token == "I":
        return token.lower()
        # uppercase I is not usually a roman numeral!

    token = token.lower()
    if len(token) < 1:
        return token
    elif token[0].isdigit() and token[-1].isdigit():
        return "#arabicnumeral"
    elif token in daysoftheweek:
        return "#dayoftheweek"
    elif token in monthsoftheyear:
        return "#monthoftheyear"
    elif token in personalnames:
        return "#personalname"
    elif token in placenames:
        return "#placename"
    elif token in romannumerals:
        return "#romannumeral"
    else:
        return token

class VolumeFromJson:

    # Mainly a data object that contains page-level wordcounts
    # for a volume.

    # Has been expanded in Jan 2017 by adding the default argument
    # pagestoinclude

    def __init__(self, volumepath, volumeid, pagestoinclude = set()):
        '''Initializes a LoadedVolume by reading wordcounts from
        a json file. By default it reads all the pages. But if
        a set of pagestoinclude is passed in, it will read only page numbers
        belonging to that set.'''

        if volumepath.endswith('bz2'):
            with bz2.open(volumepath, mode = 'rt', encoding = 'utf-8') as f:
                thestring = f.read()
        else:
            with open(volumepath, encoding = 'utf-8') as f:
                thestring = f.read()

        thejson = json.loads(thestring)

        self.volumeid = thejson['id']

        pagedata = thejson['features']['pages']
        self.numpages = len(pagedata)
        self.pagecounts = []
        self.totalcounts = Counter()
        self.totaltokens = 0
        self.bodytokens = 0

        self.sentencecount = 0
        self.linecount = 0
        typetokenratios = []

        chunktokens = 0
        typesinthischunk = set()
        # a set of types in the current 10k-word chunk; progress
        # toward which is tracked by chunktokens

        self.integerless_pages = 0
        self.out_of_order_pages = 0
        self.skipped_pages = 0
        compromise_pg = 0

        if len(pagestoinclude) < 1:
            pagestoinclude = set([x+1 for x in range(self.numpages)])
        # If an empty set was passed in, or no set was provided,
        # include all pages. the x+1 is because pages start counting
        # at one, not zero.

        for i in range(self.numpages):
            thispagecounts = Counter()
            thisbodytokens = 0
            thisheadertokens = 0
            thispage = pagedata[i]

            # There are really two ways of numbering pages. They come in an order,
            # which gives them an inherent ordinality (this is the *first* page). But
            # they also have cardinal *labels* attached, in the "seq" field. These labels
            # are usually, but not necessarily, convertible to integers. (Usually "00000001",
            # but could be "notes.") *Usually* they are == to the ordinal number,
            # but again, not necessarily.

            # In this loop, i is the ordinal page number, and cardinal_page is the cardinal
            # label; its value will be -1 if it can't be converted to an integer.

            # compromise_pg skips pages that have no integer seq, but otherwise
            # proceeds ordinally

            try:
                cardinal_page = int(thispage['seq'])
            except:
                cardinal_page = -1

            if cardinal_page > 0:
                compromise_pg += 1
            elif cardinal_page < 0:
                self.integerless_pages += 1

            if compromise_pg != cardinal_page:
                self.out_of_order_pages += 1

            if cardinal_page >= 0 and compromise_pg in pagestoinclude:

                linesonpage = int(thispage['lineCount'])
                sentencesonpage = int(thispage['body']['sentenceCount'])
                self.sentencecount += sentencesonpage
                self.linecount += linesonpage
                # I could look for sentences in the header or footer, but I think
                # that would overvalue accidents of punctuation.

                bodywords = thispage['body']['tokenPosCount']
                for token, partsofspeech in bodywords.items():
                    lowertoken = token.lower()
                    typesinthischunk.add(lowertoken)
                    # we do that to keep track of types -- notably, before nortmalizing
                    normaltoken = normalize_token(lowertoken)

                    for part, count in partsofspeech.items():
                        thisbodytokens += count
                        chunktokens += count
                        thispagecounts[normaltoken] += count

                        if chunktokens > 10000:
                            typetoken = len(typesinthischunk) / chunktokens
                            typetokenratios.append(typetoken)
                            typesinthischunk = set()
                            chunktokens = 0

                            # generally speaking we count typetoken ratios on 10000-word chunks

                headerwords = thispage['header']['tokenPosCount']
                for token, partsofspeech in headerwords.items():
                    lowertoken = token.lower()
                    normaltoken = "#header" + normalize_token(lowertoken)

                    for part, count in partsofspeech.items():
                        thisheadertokens += count
                        thispagecounts[normaltoken] += count

                # You will notice that I treat footers (mostly) as part of the body
                # Footers are rare, and rarely interesting.

                footerwords = thispage['footer']['tokenPosCount']
                for token, partsofspeech in footerwords.items():
                    lowertoken = token.lower()
                    typesinthischunk.add(lowertoken)
                    # we do that to keep track of types -- notably before nortmalizing
                    normaltoken = normalize_token(lowertoken)

                    for part, count in partsofspeech.items():
                        thisbodytokens += count
                        chunktokens += count
                        thispagecounts[normaltoken] += count

                self.pagecounts.append(thispagecounts)

                for key, value in thispagecounts.items():
                    self.totalcounts[key] += value

                self.totaltokens += thisbodytokens
                self.totaltokens += thisheadertokens
                self.bodytokens += thisbodytokens

            else:
                # print(i, cardinal_page, compromise_pg)
                self.skipped_pages += 1

        if len(typetokenratios) < 1 or chunktokens > 5000:
            # After all pages are counted, we may be left with a
            # chunk of fewer than 10000 words that we could use as further
            # evidence about typetoken ratios.

            # We do this only if we have to, or if the chunk is large
            # enough to make it reasonable evidence.

            chunktokens = chunktokens + 1     # Laplacian correction aka kludge
            typetoken = len(typesinthischunk) / chunktokens

            predictedtt = 4.549e-01 - (5.294e-05 * chunktokens) + (2.987e-09 * pow(chunktokens, 2))
            # That's an empirical quadratic regression on observed data from many genres

            extrapolatedtt =  0.2242 * (typetoken / predictedtt)
            # We infer what typetoken *would* be for a 10k word chunk of this vol, given that it's
            # typetoken for an n-word chunk.

            if extrapolatedtt > 0.6:
                extrapolatedtt = 0.6
            if extrapolatedtt < 0.1:
                extrapolatedtt = 0.1
            # Let's be realistic. We have some priors on the bounds.

            typetokenratios.append(extrapolatedtt)

        self.typetoken = sum(typetokenratios) / len(typetokenratios)
        self.sentencelength = self.bodytokens / (self.sentencecount + 1)
        self.linelength = self.totaltokens / self.linecount

        # We are done with the __init__ method for this volume.

        # When I get a better feature sample, we'll add some information about initial
        # capitalization.

    def write_volume_features(self, outpath, override = False, translator = dict()):
        ''' This writes volume features while normalizing word frequencies,
        after using a translation table to, for instance, convert American spellings
        to British.
        '''
        if os.path.isfile(outpath) and not override:
            print('Error: you are asking me to override an existing')
            print('file without explicitly specifying to do so in your')
            print('invocation of write_volume_features.')

        for word, equivalent in translator.items():
            if word in self.totalcounts:
                self.totalcounts[equivalent] += self.totalcounts.pop(word)

        with open(outpath, mode = 'w', encoding = 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['feature', 'count'])
            for key, value in self.totalcounts.items():
                if value > 0:
                    writer.writerow([key, value / self.totaltokens])
            writer.writerow(['#sentencelength', self.sentencelength])
            writer.writerow(['#typetoken', self.typetoken])
            writer.writerow(['#linelength', self.linelength])

    def get_raw_body_features(self):
        '''
        Return features sans normalization.
        '''

        outdict = Counter()

        for key, value in self.totalcounts.items():
            if not key.startswith('#header'):
                outdict[key] = value
        outdict['#sentencelength'] = self.sentencelength
        outdict['#typetoken'] = self.typetoken
        outdict['#linelength'] = self.linelength

        return outdict, self.bodytokens

    def get_volume_features(self):
        '''
        Just like write_volume_features, except we return them
        as a dictionary.
        '''

        outdict = Counter()
        if self.totaltokens < 1:
            return outdict, 0

        else:

            for key, value in self.totalcounts.items():
                outdict[key] = value / self.totaltokens
            outdict['#sentencelength'] = self.sentencelength
            outdict['#typetoken'] = self.typetoken
            outdict['#linelength'] = self.linelength

            return outdict, self.totaltokens

    def append_volume_features(self, outpath):
        ''' This is probably the way to do it. Initialize the file with
        a header, and then add a bunch of volumes to the same file,
        incorporating a column that distinguishes them by docid.
        '''

        with open(outpath, mode = 'a', encoding = 'utf-8') as f:
            writer = csv.writer(f)
            for key, value in self.totalcounts.items():
                writer.writerow([self.volumeid, key, value / self.totaltokens])
            writer.writerow([self.volumeid, '#sentencelength', self.sentencelength])
            writer.writerow([self.volumeid, '#typetoken', self.typetoken])
            writer.writerow([self.volumeid, '#linelength', self.linelength])


def log_tokens_for_page(pagejson, pagedict, typesonpage, ficcount, headerflag):
    '''
    Takes data from the pagejson and logs it appropriately in pagedict
    and typesonpage.
    '''

    global ficwords

    for token, partsofspeech in pagejson.items():

        if token.istitle():
            titleflag = True
        else:
            titleflag = False

        if token.isupper():
            upperflag = True
        else:
            upperflag = False

        lowertoken = token.lower()
        typesonpage.add(lowertoken)
        # we do that to keep track of types -- notably, before normalizing

        normaltoken = normalize_token_for_page(token)
        # normalizing also lowercases the token, but we don't
        # want to *send in* a lowercased token

        for part, count in partsofspeech.items():
            if headerflag:
                pagedict['headertokens'] += count
            else:
                pagedict['bodytokens'] += count

            if upperflag:
                pagedict['uppercase'] += count
            if titleflag:
                pagedict['titlecase'] += count

            if lowertoken in ficwords:
                ficcount += count

            pagedict['tokens'][normaltoken] += count

    return ficcount

class PagelistFromJson:

    # A data object that contains page-level wordcounts
    # for a volume,

    def __init__(self, volumepath, volumeid):
        '''initializes a LoadedVolume by reading wordcounts from
        a json file'''

        if volumepath.endswith('bz2'):
            with bz2.open(volumepath, mode = 'rt', encoding = 'utf-8') as f:
                thestring = f.read()
        else:
            with open(volumepath, encoding = 'utf-8') as f:
                thestring = f.read()

        thejson = json.loads(thestring)
        assert thejson['id'] == volumeid
        # I require volumeid to be explicitly passed in,
        # although I could infer it, because I don't want
        #any surprises.

        self.volumeid = thejson['id']

        pagejsons = thejson['features']['pages']
        self.numpages = len(pagejsons)
        self.pages = []
        self.features = []

        # in this data structure, a volume is a list of pages

        for i in range(self.numpages):
            pagedata = dict()
            # each page  is a dictionary that contains categories of
            # features, most obviously wordcounts:
            pagedata['tokens'] = Counter()

            pagedata['bodytokens'] = 0
            pagedata['titlecase'] = 0
            pagedata['uppercase'] = 0
            pagedata['headertokens'] = 0
            self.pages.append(pagedata)

        for i in range(self.numpages):
            pagedata = self.pages[i]
            thispage = pagejsons[i]

            typesonpage = set()
            ficcount = 0

            pagedata['lines'] = int(thispage['lineCount'])
            pagedata['sentences'] = int(thispage['body']['sentenceCount'])
            # I could look for sentences in the header or footer, but I think
            # that would overvalue accidents of punctuation.

            bodywords = thispage['body']['tokenPosCount']
            ficcount = log_tokens_for_page(bodywords, pagedata, typesonpage, ficcount, headerflag = False)

            headerwords = thispage['header']['tokenPosCount']
            ficcount = log_tokens_for_page(headerwords, pagedata, typesonpage, ficcount, headerflag = True)

            footerwords = thispage['footer']['tokenPosCount']
            ficcount = log_tokens_for_page(footerwords, pagedata, typesonpage, ficcount, headerflag = True)

            pagefeatures = dict()
            # We don't directly return token counts, but normalize them
            # in various ways

            totaltokens = pagedata['bodytokens'] + pagedata['headertokens']

            if totaltokens > 0:
                for key, value in pagedata['tokens'].items():
                    pagefeatures[key] = value / totaltokens

            pagefeatures['#totaltokens'] = totaltokens

            if totaltokens > 0:
                pagefeatures['#typetoken'] = len(typesonpage) / totaltokens
            else:
                pagefeatures['#typetoken'] = 1

            pagefeatures['#absfromedge'] = min(i, self.numpages - i)
            pagefeatures['#pctfromedge'] = pagefeatures['#absfromedge'] / self.numpages


            pagefeatures['#absupper'] = pagedata['uppercase']
            if totaltokens > 0:
                pagefeatures['#pctupper'] = pagedata['uppercase'] / totaltokens
            else:
                pagefeatures['#pctupper'] = 0.5

            pagefeatures['#abstitle'] = pagedata['titlecase']
            if totaltokens > 0:
                pagefeatures['#pcttitle'] = pagedata['titlecase'] / totaltokens
            else:
                pagefeatures['#pcttitle'] = 0.5

            if pagedata['lines'] > 0:
                pagefeatures['#linelength'] = totaltokens / pagedata['lines']
            else:
                pagefeatures['#linelength'] = 10

            if totaltokens > 0:
                pagefeatures['#ficpct'] = ficcount / totaltokens
            else:
                pagefeatures['#ficpct'] = 0

            self.features.append(pagefeatures)

        # Some features also get recorded as Z values normalized by the mean and
        # standard deviation for this volume.

        tonormalize = ['#typetoken', '#pcttitle', '#linelength', '#totaltokens', '#ficpct']
        for feature in tonormalize:
            values = np.zeros(self.numpages)
            for i in range(self.numpages):
                pagefeatures = self.features[i]
                values[i] = (pagefeatures[feature])

            meanval = np.mean(values)
            stdval = np.std(values) + .0001

            normalizedfeature = feature + 'normed'
            for i in range(self.numpages):
                self.features[i][normalizedfeature] = (self.features[i][feature] - meanval) / stdval

        # We are done with the __init__ method for this volume.

        # When I get a better feature sample, we'll add some information about initial
        # capitalization.

    def get_feature_list(self):
        '''
        Returns a list where each page is represented as a dictionary of features.
        Features should already be normalized in all the ways we're going to
        normalize them.
        '''

        return self.features

class LiteralVolumeFromJson:

    # Mainly a data object that contains page-level wordcounts
    # for a volume.

    def __init__(self, volumepath, volumeid):
        '''initializes a LoadedVolume by reading wordcounts from
        a json file'''

        if volumepath.endswith('bz2'):
            with bz2.open(volumepath, mode = 'rt', encoding = 'utf-8') as f:
                thestring = f.read()
        else:
            with open(volumepath, encoding = 'utf-8') as f:
                thestring = f.read()

        thejson = json.loads(thestring)
        assert thejson['id'] == volumeid
        # I require volumeid to be explicitly passed in,
        # although I could infer it, because I don't want
        #any surprises.

        self.volumeid = thejson['id']

        pagedata = thejson['features']['pages']
        self.numpages = len(pagedata)
        self.pagecounts = []
        self.totalcounts = Counter()
        self.totaltokens = 0

        for i in range(self.numpages):
            thispagecounts = Counter()
            thisbodytokens = 0
            thisheadertokens = 0
            thispage = pagedata[i]

            linesonpage = int(thispage['lineCount'])
            sentencesonpage = int(thispage['body']['sentenceCount'])
            # I could look for sentences in the header or footer, but I think
            # that would overvalue accidents of punctuation.

            bodywords = thispage['body']['tokenPosCount']
            for normaltoken, partsofspeech in bodywords.items():

                for part, count in partsofspeech.items():
                    thisbodytokens += count
                    thispagecounts[normaltoken] += count

            self.pagecounts.append(thispagecounts)

            for key, value in thispagecounts.items():
                self.totalcounts[key] += value

            self.totaltokens += thisbodytokens

        # We are done with the __init__ method for this volume.

        # When I get a better feature sample, we'll add some information about initial
        # capitalization.

    def write_volume_features(self, outpath, override = False):
        if os.path.isfile(outpath) and not override:
            print('Error: you are asking me to override an existing')
            print('file without explicitly specifying to do so in your')
            print('invocation of write_volume_features.')

        with open(outpath, mode = 'w', encoding = 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['feature', 'count'])
            for key, value in self.totalcounts.items():
                writer.writerow([key, value / self.totaltokens])
            writer.writerow(['#sentencelength', self.sentencelength])
            writer.writerow(['#typetoken', self.typetoken])
            writer.writerow(['#linelength', self.linelength])

    def get_volume_features(self):
        '''
        Just like write_volume_features, except we return them
        as a dictionary.
        '''

        if self.totaltokens < 1:
            return Counter(), 0

        else:

            return self.totalcounts, self.totaltokens

if __name__ == "__main__":

    meta = pd.read_csv('/Users/tunder/Dropbox/python/train20/bzipmeta.csv', dtype = 'object', index_col = 'docid')
    for index, row in meta.iterrows():
        inpath = row['filepath']
        vol = VolumeFromJson(inpath, index)
        outpath = '/Volumes/TARDIS/work/train20/' + utils.clean_pairtree(index) + '.csv'
        vol.write_volume_features(outpath, override = True)



