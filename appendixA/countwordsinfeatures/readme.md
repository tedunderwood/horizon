count words in features
========================

Instead of working directly with texts, this works with jsons derived from the [HTRC Extracted Features Dataset](https://wiki.htrc.illinois.edu/display/COM/Extracted+Features+Dataset). See that page for information on downloading the list of files you want. With a tiny bit of ingenuity, it is not hard to use my metadata to create a list of files, compare that list of files to the complete list of paths at HTRC, and generate list of paths which can be used to get exactly the files you need from HTRC. So in principle this part is very beautifully reproducible. (With a tiny bit of ingenuity.)

The output is a list of features used for classification, not all of which are literally tokens. E.g., the output includes things like #sentencelength, #linelength, and #dayoftheweek.

Usage here is not as pretty as tokenizetexts; you'll have to edit the

    if __name__ == "__main__":

clause at the end of the script.

BUT before that will work, you'll also need to get [a lot of rulesets from my DataMunging repo,](https://github.com/tedunderwood/DataMunging/tree/master/rulesets) and change the paths in parsefeaturejsons so they point to your local copy of those rules. Sorry.

