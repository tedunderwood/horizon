count words in texts
====================

The name is a bit of a misnomer, because the real goal here is to generate a list of features for classification, not all of which are literally tokens. E.g., the output includes things like #capsprob and #wordlength.

As the script explains, usage is basically

python3 tokenizetexts.py sourcefolder destinationfolder

BUT before that will work, you'll need to get [a lot of rulesets from my DataMunging repo,](https://github.com/tedunderwood/DataMunging/tree/master/rulesets) and change the paths in tokenizetexts so they point to your local copy of those rules. Sorry.

