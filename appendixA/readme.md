Appendix A : Data and reproducibility
=====================================

This folder contains code used to count words, and a draft of Appendix A, but this readme file is also a good place to start thinking about the gritty details of reproducing workflows in *The Curved Horizon of Literary History.*

Goals
-----

My goals in this repository are

1. To let people without programming experience simply inspect the list of texts used in a particular chapter, 
2. To make it possible for someone with moderate programming experience to actually reproduce calculations and figures, working from original data in the form of word counts.
3. To provide code that someone super-scrupulous could use to reproduce the word counting.

Limits
------

There are also some things I can't guarantee. 

1. The original texts are often in copyright, or covered by other IP contracts, so I can't share readable texts.
2. I don't intend to provide "tools," designed to be useful in other research projects. This is just code that I actually used in the process of answering a particular set of questions.
3. I also, frankly, can't even guarantee that everything is going to run in a simple push-button way. I've tried to make paths relative to the repo, but I may not have always succeeded; you might have to edit some things before they run.

Structure
---------

This is not a single article; it's a book covering five years of research. The data changed along the way, my assumptions about methods changed, and the goals of different chapters are in any case different. So I have not attempted a tightly unified structure, where all the chapters refer back to one central dataset. Instead, each chapter uses a slightly different sample. For a broader description of my decision not to stabilize sampling, see Appendix A itself.

Attempts to reproduce a result should ordinarily begin at the chapter level. Those chapter repos are usually organized around documentation for figures, so the easiest way to identify data and code you're interested in may be to identify a figure that used the data, and trace it backward to its sources.

I have usually provided an R script that created the figure, plus the table it immediately used. In many cases that table is itself the result of a modeling or transformation process, and I have tried to guide you to the appropriate code. But the original source data used in *that* process may or may not be (immediately) included in the repo. It's often a folder of several thousand wordcount files, which may be slightly too big to fit in the 1GB github size limits. So I have tried to provide a link to those source files, packaged up as .tar.gz; to re-run the modeling process, you'll need to unpackage them and place them in the folder indicated. Right now these links point to my Dropbox; when the book actually goes to print, they will point to something more durable like figshare or zenodo.

In some cases, though, you may be less interested in re-running the original modeling than in identifying the books used. Check the metadata folder, and check the code to find out which metadata file was used for the process you're interested in.

Stochastic character of modeling
--------------------------------

A lot of the models produced in this book use a Python script called versatiletrainer.py; generally they use the version in horizon/logistic, although chapter 4 actually uses its own files in the chapter4 folder. (As I mentioned above, this is not a tightly refactored structure!) 

In any case, versatiletrainer is not designed to produce the same result every time you run it. Randomness comes in when files are selected, e.g if there are more files available in the negative class than needed to match positive examples. Randomness also plays a role in the modeling process itself. So you should not be surprised if you reproduce the modeling and get a result that is .1% - .5% higher or lower than the figure cited in the book.

I thought about setting this up so it's reproducible in a more airtight way, with a random number seed so you get exactly the number I got if you use the same inputs. But there are no arguments in the book that actually depend on this level of quantitative precision, and actually I felt it was more important to acknowledge that the Brownian motion is there.

Similarly, you'll find that the coefficients produced by your models may not exactly line up with the coefficients in mine. If we were interpreting models by looking at the top and bottom ten words in the list of coefficients, this would be a problem. But that's why, in fact, the text of the book urges people *not* to interpret models with thousands of variables purely by looking at ten at the top or bottom--but to use more robust approaches.

