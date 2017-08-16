#!/usr/bin/env python3

# tokenizetexts.py

# This is my own custom-rolled tokenizer,
# which allows me to control various
# aspects of the tokenization process so
# I can test options.

# Overall, the emphasis here is on providing
# a set of normalized features for supervised
# learning. It's definitely not concerned to
# handle English word boundaries in an idiomatic
# way.

# It is also NOT FAST. I use multiprocessing to
# speed it up a little, but more optimization is
# needed. If I find that bigrams don't actually help,
# cutting them out might do a lot to speed things
# up.

# USAGE
# python3 tokenizetexts.py sourcefolder_of_texts destination_for_tsvs

import csv, os, sys, re, glob

from collections import Counter

from multiprocessing import Pool

def get_rules(ruledirectory = '/Users/tunder/Dropbox/DataMunging/rulesets/'):
    '''
    Tokenizing is going to depend on a variety of wordlists and rules.
    This function loads them from a directory.
    '''

    specialfeatures = {"#arabicnumeral", "#romannumeral", "#dayoftheweek", "#monthoftheyear", "#personalname", "#placename"}

    lexiconpath = os.path.join(ruledirectory, 'MainDictionary.txt')
    lexicon = set()
    with open(lexiconpath, encoding = 'utf-8') as f:
        for line in f:
            fields = line.split('\t')
            lexicon.add(fields[0])

    if '' in lexicon:
        lexicon.remove('')
        # I just want to make sure that's not in there through some mistake

    for ft in specialfeatures:
        lexicon.add(ft)

    namepath = os.path.join(ruledirectory, 'PersonalNames.txt')
    with open(namepath, encoding = 'utf-8') as f:
        personalnames = set([x.strip().lower() for x in f.readlines()])

    placepath = os.path.join(ruledirectory, 'PlaceNames.txt')
    with open(placepath, encoding = 'utf-8') as f:
        placenames = set([x.strip().lower() for x in f.readlines()])

    romanpath = os.path.join(ruledirectory, 'RomanNumerals.txt')
    with open(romanpath, encoding = 'utf-8') as f:
        romannumerals = set([x.strip().lower() for x in f.readlines()])

    correctionrules = dict()
    correctionpath = os.path.join(ruledirectory, 'CorrectionRules.txt')
    with open(correctionpath, encoding = 'utf-8') as f:
        reader = csv.reader(f, delimiter = '\t')
        for row in reader:
            correctionrules[row[0]] = row[1]

    variants = dict()
    variantpath = os.path.join(ruledirectory, 'VariantSpellings.txt')
    with open(variantpath, encoding = 'utf-8') as f:
        reader = csv.reader(f, delimiter = '\t')
        for row in reader:
            variants[row[0]] = row[1]

    contractionrules = dict()
    contractionpath = os.path.join(ruledirectory, 'Contractions.tsv')
    with open(contractionpath, encoding = 'utf-8') as f:
        reader = csv.reader(f, delimiter = '\t')
        for row in reader:

            # This is a little tricky. We get a row like
            # wasn  '   t   wasn't  wasn_t
            # lookup will be triggered by the single quote
            # our goal is to create a hashtable that maps
            # the two parts of the contraction to the whole
            # word

            contractedtuple = (row[0], row[2])
            contractionrules[contractedtuple] = row[3]

    daysoftheweek = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    monthsoftheyear = {'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'}

    bigrampath = os.path.join(ruledirectory, 'top_fiction_bigrams.tsv')
    top5kbigrams = set()
    bigramlex = set()
    ctr = 0
    with open(bigrampath, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            big = fields[0]
            top5kbigrams.add(big)
            bparts = big.split('_')
            if len(bparts) > 2:
                bigramlex.add(bparts[1])
                bigramlex.add(bparts[2])
            else:
                print(bparts)
            ctr += 1
            if ctr >= 5000:
                break


    return lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules, top5kbigrams, bigramlex

def normalize_token(token, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals):
    ''' Normalizes a token by lowercasing it and by bundling
    certain categories together. The lists of personal and place names
    are never going to be all-inclusive; you have to be aware of that,
    and deactivate this in corpora where it could pose a problem.
    '''

    token = token.lower()
    if len(token) < 1:
        return token

    if token in correctionrules:
        token = correctionrules[token]

    if token in variants:
        token = variants[token]

    if token[0].isdigit() and token[-1].isdigit():
        return "#arabicnumeral"
    elif token in romannumerals:
        return "#romannumeral"
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

def tokenize_line(line, previous_word, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules):
    '''
    Breaks a line into words wherever non-word ~[a-z0-9] characters occur. This
    absolutely means that hyphenated words will be split. The only exception is
    that contractions (like "can't") are kept together.

    We count the words, and also save the punctuation marks that are breaking works
    and count those as well. Finally we count *bigrams*, which are defined here as
    sequences of two alphanumeric tokens (punctuation marks are not included).

    Saving the alphanumeric words in a counter separate from the punctuation marks allows
    us to calculate word frequencies as a fraction of words, and punctuation frequencies as
    a fraction of punctuation, and then separately report the fraction of all tokens
    that are punctuation marks. This is a way of factoring sentence length out as a
    feature separate from the multinomial distributions of words and punctuation across
    possible word-space and punctuation-space.
    '''

    wordcounts = Counter()
    punctcounts = Counter()
    capitalized = 0
    lengths = []
    allwords = 0
    allpunct = 0
    bigrams = Counter()

    line = line.strip()
    line = line.replace('_', ' ')
    # because we don't want underscores counted as "word characters"

    line = line.replace("`", "'")
    line = line.replace("‘", "'")
    line = line.replace("’", "'")

    line = line.replace('“', '"')
    line = line.replace('”', '"')

    # In a world where we were trying to identify dialogue, opening
    # and closing curly quotes might be valuable. As features, they
    # are noise.

    words = re.split('(\W)', line)

    wordlen = len(words)
    skipnext = False
    twowordsback = previous_word

    for i, w in enumerate(words):

        if len(w) < 1 or w == ' ':
            continue
            # empty strings ignored

        if skipnext:
            skipnext = False
            continue

        if w == "'" and i < (wordlen - 1):

            next = words[i + 1].lower()
            contractedtuple = (previous_word , next)

            if contractedtuple in contractionrules:
                if previous_word in wordcounts:
                    wordcounts[previous_word] -= 1
                skipnext = True
                contraction = contractionrules[contractedtuple]

                wordcounts[contraction] += 1
                allwords += 1

                if twowordsback in lexicon:
                    bigram = "#bi_" + twowordsback + '_' + contraction
                    bigrams[bigram] += 1

                twowordsback = previous_word
                previous_word = contraction

                # we don't increment wordcounts
                # or capitalized because that
                # presumably already happened

            else:
                # it's just a single quote
                punctcounts[w] += 1
                allpunct += 1

        elif w.isalnum():
            # if alphanumeric add to wordcounts

            if w[0].isupper():
                capitalized += 1

            lengths.append(len(w))

            normalized_word = normalize_token(w, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals)

            wordcounts[normalized_word] += 1
            allwords += 1

            if previous_word in lexicon and normalized_word in lexicon:
                bigram = "#bi_" + previous_word + '_' + normalized_word
                bigrams[bigram] += 1

            twowordsback = previous_word
            previous_word = normalized_word

        else:
            # add to a separate counter for punctuation
            punctcounts[w] += 1
            allpunct += 1

    # notice that we return previous_word (the last word processed), so that it can be
    # used as an argument the next time this function is invoked

    return wordcounts, punctcounts, capitalized, allwords, allpunct, lengths, previous_word, bigrams

class FeatureVector:

    def __init__(self, linelist, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules):
        ''' To create a feature vector, you pass in a list of lines to be tokenized,
        plus a whole bunch of rules and wordlists that we use to categorize tokens.
        '''

        self.wordcounts = Counter()
        self.punctcounts = Counter()
        self.capitalized = 0
        self.totalnumwords = 0
        self.totalnumpunct = 0
        self.allwordlengths = []
        self.allbigrams = Counter()

        previous_word = ''

        for l in linelist:
            linewords, linepunct, linecaps, linenumwords, linenumpunct, linelens, previous_word, linebigrams = tokenize_line(l, previous_word, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules)

            self.wordcounts = self.wordcounts + linewords
            self.punctcounts = self.punctcounts + linepunct
            self.capitalized = self.capitalized + linecaps
            self.totalnumwords = self.totalnumwords + linenumwords
            self.totalnumpunct = self.totalnumpunct + linenumpunct
            self.allwordlengths.extend(linelens)
            self.allbigrams = self.allbigrams + linebigrams

    def write_normalized_features(self, outpath, top5kbigrams, bigramlex):
        '''
        This writes features to file. Importantly, features are written *already normalized*
        by total wordcount, or punctuation count. The reason I do this is that it simplifies
        processing when you're building a model, especially if some of the features are
        statistical metrics that *should not* be divided by total wordcount. If you write
        raw word frequencies, you're going to have to remember later which features get divided
        by total word frequency.

        Special features include:
            #capsprob - the fraction of words capitalized (for any reason, and whether
                          all upper or only titlecased)
            #punctprob - the proportion of tokens that are punctuation marks
            #wordlength - mean length of all alphanumeric tokens
            #fogindex - wordlength * (commas / periods). This is meant to be a rough proxy
                        for wordlength * sentence length. I don't actually calculate
                        sentence length, because it's a pain, but it will leave traces in
                        capsprob, punctprob, and fogindex.
            #bigramcommon - prob a bigram came from list of 5k common bigrams
            #unigramcommon - prob any word came from list of all words in the bigram list
            #seqpredictable - bigramcommon / (unigramcommon ** 2)
                              This roughly reflects conditional entropy. It will be high
                              where words tend to occur in conventional pairings, and low
                              when there are lots of common words used in uncommon
                              sequences
        '''

        outlines = []

        if self.totalnumwords == 0 or self.totalnumpunct == 0:
            return False
            # can't do this if we have nothing to write

        if os.path.isfile(outpath):
            print('Error: attempt to overwrite existing feature file.')
            return False

        cap_prob = self.capitalized / self.totalnumwords
        line = "#capsprob" + '\t' + str(cap_prob)
        outlines.append(line)

        alltokens = self.totalnumwords + self.totalnumpunct

        punct_prob = self.totalnumpunct / alltokens
        line = "#punctprob" + '\t' + str(punct_prob)
        outlines.append(line)

        avg_word_length = sum(self.allwordlengths) / len(self.allwordlengths)
        line = "#wordlength" + '\t' + str(avg_word_length)
        outlines.append(line)

        wordsintopbigramlex = 0

        for word, count in self.wordcounts.items():

            frequency = count / self.totalnumwords
            line = word + '\t' + str(frequency)
            outlines.append(line)
            if word in bigramlex:
                wordsintopbigramlex += count

        for punct, count, in self.punctcounts.items():

            frequency = count / self.totalnumpunct
            line = "#punct_" + punct + '\t' + str(frequency)
            outlines.append(line)

        commaperiod = (self.punctcounts[','] + 1) / (self.punctcounts['.'] + 1)
        fogindex = commaperiod * avg_word_length
        line = "#fogindex" + '\t' + str(fogindex)
        outlines.append(line)

        totalbigrams = sum(self.allbigrams.values())
        bigramsintop5k = 0

        for bigram, count in self.allbigrams.items():

            if bigram in top5kbigrams:
                frequency = count / totalbigrams
                line = bigram + '\t' + str(frequency)
                outlines.append(line)
                bigramsintop5k += count

        bigramcommonnness = bigramsintop5k / totalbigrams
        line = "#bigramcommon" + '\t' + str(bigramcommonnness)
        outlines.append(line)

        # We also calculate the percentage of single words that came from the
        # range of words included in those top5k bigrams

        unigramcommonness = wordsintopbigramlex / self.totalnumwords
        line = "#unigramcommon" + '\t' + str(unigramcommonness)
        outlines.append(line)

        sequencepredictability = bigramcommonnness / (unigramcommonness ** 2)
        # Generally speaking, bigram occurrence ought to be proportional
        # to the square of the probability that component unigrams will
        # occur. This would be true, at any rate, if our list of bigrams
        # contained all possible permutations of the unigrams. But of
        # course it doesn't, which is the point.

        line = "#seqpredictable" + '\t' + str(sequencepredictability)
        outlines.append(line)

        with open(outpath, mode = 'w', encoding = 'utf-8') as f:
            for line in outlines:
                f.write(line + '\n')

        return True

    def get_top_bigrams(self, n):
        bigramstoreturn = self.allbigrams.most_common(n)
        return bigramstoreturn

def get_vol_bigrams(tentuple):
    '''
    This function is designed explicitly for multiprocessing. It takes a tuple with a linelist
    for a particular volume, plus a bunch of rules and wordlists, and uses all that data to create
    a FeatureVector.
    '''
    lines, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules = tentuple
    vector = FeatureVector(lines, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules)
    these_bigrams = vector.get_top_bigrams(10000)
    return these_bigrams

def print_features(thirteentuple):
    '''
    This function is designed explicitly for multiprocessing. It takes a tuple with a linelist
    for a particular volume, plus a destination path, and a bunch of rules and wordlists, and uses
    all that data to create a FeatureVector. Then it tells the FeatureVector to print a
    feature file to the designated destinationpath. Because absolutely everything you need is
    packaged in the tuple, you can map tuples across a pool of worker processes.
    '''
    lines, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules, top5kbigrams, bigramlex, destinationpath = thirteentuple
    vector = FeatureVector(lines, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules)
    vector.write_normalized_features(destinationpath, top5kbigrams, bigramlex)

    # the return value has no real meaning here; the point i

    return True

if __name__ == "__main__":

    arguments = sys.argv

    lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules, top5kbigrams, bigramlex = get_rules()

    if arguments[1] == "--folder":
        sourcefolder = arguments[2]
        destinationfolder = arguments[3]
        if not os.path.isdir(sourcefolder) or not os.path.isdir(destinationfolder):
            print('What kind of fool do you take me for? Those are not')
            print('both valid directories.')
            sys.exit(0)

        if not sourcefolder.endswith('/'):
            sourcefolder += '/'
        if not destinationfolder.endswith('/'):
            destinationfolder += '/'
        paths = glob.glob(sourcefolder + '*.txt')

        ctr = 0
        for floor in range(970, 1100, 200):
            print(ctr)
            ctr += 1
            linelists = []
            ceiling = floor + 200
            if ceiling > len(paths):
                ceiling = len(paths)
            print(ceiling)
            for p in paths[floor: ceiling]:
                docid = p.replace(sourcefolder, '')
                docid = docid.replace('.txt', '')
                destinationpath = destinationfolder + docid + '.tsv'
                if os.path.isfile(destinationpath):
                    print(destinationpath + ' already exists.')
                    continue
                with open(p, encoding = 'utf-8') as f:
                    lines = f.readlines()
                    linelists.append((lines, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules,top5kbigrams, bigramlex, destinationpath))

            pool = Pool(processes = 12)
            res = pool.map_async(print_features, linelists)
            res.wait()

            resultlist = res.get()

            pool.close()



    elif arguments[1] == "--bigrams":
        paths = glob.glob('/Users/tunder/Dropbox/fiction/newtexts/*.txt')

        top_bigrams = Counter()

        ctr = 0
        for floor in range(0, 1000, 100):
            linelists = []
            for p in paths[floor: (floor + 50)]:
                with open(p, encoding = 'utf-8') as f:
                    lines = f.readlines()
                    linelists.append((lines, lexicon, personalnames, placenames, daysoftheweek, monthsoftheyear, correctionrules, variants, romannumerals, contractionrules))

            pool = Pool(processes = 12)
            res = pool.map_async(get_vol_bigrams, linelists)
            res.wait()

            resultlist = res.get()

            ctr +=1
            print(ctr)

            for bigram_tuple_list in resultlist:

                for bigram, count in bigram_tuple_list:
                    top_bigrams[bigram] += count

            pool.close()

        with open('top_fiction_bigrams.tsv', mode = 'w', encoding = 'utf-8') as f:
            f.write('bigram' + '\t' + 'count' + '\n')
            for bigram, count in top_bigrams.most_common(10000):
                f.write(bigram + '\t' + str(count) + '\n')









