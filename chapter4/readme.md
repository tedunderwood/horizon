Chapter Four
============

"Metamorphoses of gender."

This chapter uses a lot of voluminous data that couldn't fit in the repository. For the early figures based on predictive models, you will usually need to unpack [**data_for_chapter4a.tar.gz**](https://www.dropbox.com/s/tut72d5ghx8tmz9/data_for_chapter4a.zip?dl=0), which should produce a folder named **sourcefiles**. For the later figures based on more direct counting, unpack [**data_for_chapter4b.tar.gz**](https://www.dropbox.com/s/amz2pds7v4b0oq3/data_for_chapter4b.zip?dl=0), which should produce a folder called **data**. All of this is derived data; if you want to actually work from original texts, you would need to use my metadata to request files from HathiTrust, and analyze them using [BookNLP.](https://github.com/dbamman/book-nlp)

figures
--------

Most of the figures were produced by a script in **rplots.** I'm not going to list the specific R script in each case, because the naming convention is transparent. E.g., figure 4.1 was produced by **rplots/C4Fig1accuracybydecade.R**

**Figure 4.1** The data here is created originally by **train_models/reproduce_character_models.py**; select the "decade_grid" option. This will produce a file called **dataforR/decadegrid.tsv.** To condense that into a data frame that can be used for plotting, you need to run **plot_scripts/get_decade_optimums.py.**

**Figures 4.2, 4.3, 4.4, 4.5, and 4.6** The data for all of these figures is **dataforR/diff_matrix.tsv**. This is created by **plot_scrips/make_diff_matrix.py**, using data from **data_for_chapter4b.tar.gz**, which needs to go in the **data** folder.

**Figure 4.7** Uses **dataforR/differentiation_plot.csv**, which was produced immediately by a script in plot_scripts: **create_differentiation_plot_data.py**. But this, in turn relies on **data/gender_probs_for_diff.py,** which was ultimately created by **train_models/apply_model_to_characters.py**, which *in turn* (sorry) relies on models in the **modelused** directory and character_tables in **data.*

**Figure 4.8** is based directly on summary files in **data**.

**Figure 4.9** uses **dataforR/authorratios.csv** and **dataforR/pubweeklyerrorbars.csv**, both of which are produced by **plot_scripts/pubweekly_gender_plots.py.** This in turn draws on evidence in the **pubweekly, pre23hathi,** and **post22hathi** directories.

**Figure 4.10** is based on **dataforR/nonfiction_stack_graph.csv**, which in turn is produced by **plot_scripts/nonfiction_stack_graph.py,** and uses the file **nonfiction_genders.tsv**, which will needto be unpacked from data_for_chapter4b.tar.gz.

If you want to understand the underlying data,
----------------------------------------------
The most complete derived data (that we can legally share) are tabular representations of the words associated with individual characters: character_table_18c19c.tsv and character_table_post1900.tsv. At 4GB total, these are too big for this repository are made available instead as data_for_chapter4c.tar.gz/

Much of the analysis of publishing trends in the second part of the article can be reproduced using **filtered_fiction_metadata.csv** in the **metadata** subdirectory. The scripts to reproduce that analysis are under **/plot_scripts**.

We also used data from the Chicago Text Lab as a contrastive touchstone in several places, but we have only provided a very high-level (yearly) summary of that data here. Contact Hoyt Long or Richard So for more information.

If you want to reproduce predictive modeling,
---------------------------------------------
Most of the modeling was run on a subset of 84,000 characters balanced to have (where possible) 2000 characters with masculine names and 2000 characters with feminine names for each decade. (Total numbers are slightly lower in the late 18c; note also that 1780-1799 have been aggregated and treated as a single decade.) Characters were selected so that the median description length for a character was as close as possible to 54 words for both genders, in each decade. The data we used is available in **data_for_chapter4a.tar.gz.**

If you want to reproduce the selection process itself, you would need to run **select_balanced_subset.py** in the **transform_data** directory. Alternatively, you could work with the **balanced_character_subset.tar.gz** provided here (which is the subset of 84,000 we actually used). Unpack that, and run **reproduce_character_models.py** in the **train_models** subdirectory. See that script for usage instructions.

If you want to explore the gendering of specific words,
-------------------------------------------------------
as we do in figures 11-15, you have two options. An [interactive visualization constructed by Nikolaus Parulian](http://ec2-35-165-215-214.us-west-2.compute.amazonaws.com/dataviz/genderviz) allows you to explore online. Alternatively, you can edit the code in the scripts for figures 10-14 available under **/plotscripts/rplots** or simply write your own code to visualize the data in **dataforR/diff_matrix.csv**, which reports the yearly difference between normalized frequencies for men and women.

Brief descriptions of subdirectories.
======================================
The five most important subdirectories are listed first, then alphabetically.

plot_scripts
------------
Code used to generate visualizations in the final article. This may be the first place to look for options to reproduce or tweak particular figures. Generally there is an initial transformation in Python, which generates a file in **dataforR**. Then a file in **plot_scripts/rplots** does the final visualization in R/ggplot2.

dataforR
--------
Holds the final stage of data, immediately before visualization in R. In particular, this includes a **diff_matrix** that can be used to explore the gendering of individual words.

transform_data
--------------
Scripts that transform the raw jsons generated by BookNLP into intermediate tabular data files, and then select characters from those files for modeling.

train_models
------------
Scripts for predictive modeling.

metadata
--------
Contains metadata for volumes used in this project, along with a discussion of metadata error. The central metadata file is **filtered_fiction_metadata.csv.**

alphabetic hereafter:
---------------------

bestsellergender
----------------
Some data on bestsellers, used in one figure.

blogpost
--------
Scripts used to calculate confidence intervals and plot visualizations in the blog post ["The Gender Balance of Fiction, 1800-2007,"](https://tedunderwood.com/2016/12/28/the-gender-balance-of-fiction-1800-2007/) 2016. Mostly deprecated now.

chicago
-------
A terse, high-level summary of character data from the Chicago Novel Corpus. Note that the  Chicago dataset has expanded and changed since we used it in 2015.

error
-----
A brief discussion of sources of error in the project.

future_work
------------
Further analysis of the data, not included in the published article, or fully documented yet.

genre_experiment
----------------
Checking to see whether the rise of genre fiction might explain changes in the gender balance of the larger dataset. Not directly used in the article version; was displaced by pubweekly, which answered a similar question.

images
------
Images used in the article, with notes on sourcing.

lexicons
--------
Stoplists and other data files, mostly used in transformation of dialogue, which doesn't turn out to be crucial in our final article.

oldcode
-------
deprecated

post22hathi
-----------
Yearly summaries, mostly not used directly in the final analysis, except for post22_character_data.csv.

pre23hathi
----------
Yearly summaries, mostly not used directly in the final analysis, except for pre23_character_data.csv.

pubweekly
---------
Data from spot checking Publisher's Weekly to see how far academic libraries diverge from other ways of sampling the past.

vizdata
--------
Metadata and data used in an interactive visualization.

yearlysummaries
---------------
Aggregated yearly word counts, broken out by author gender and character gender, and by the grammatical role of the word. This is mostly deprecated; I don't think this data is used directly in the current article-reproduction workflow.
