Chapter Two code
================

The workhorse here is **reproduce.py**. This is unfortunately a long and messy script of 860 lines, calling equally long and messy scripts up in horizon/logistic. But basically, the script will do lots of different things, depending on the argument (option) you pass to it. For instance,

    USAGE:
    python3 reproduce.py allSF

will give you results for 'allSF.'

Here are some options you might want to invoke.

**detectnewgatesensation** gets you the data behind figure 2.1

**allSF** gets you the data behind fig 2.2.

**SFpaceofchange** and **detectivepaceofchange**, together, generate data used in fig 2.3.

Other options pose questions that substantiate particular figures mentioned in the text.

For this to work, you'll need to unpack the data in
data_for_chapter2.tar.gz, and place it in
horizon/chapter2/sourcefiles/

**find_surprises.py** is an odd little script that I used to understand the accelerated pace of change for science fiction in the middle of the 20c. It produced plotdata/sfsurprises, which is not actually used to plot anything.
