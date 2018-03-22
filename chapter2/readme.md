Chapter Two
===========

"The lifespans of genres."

To understand how to reproduce a given figure, use the key below. If you want to reproduce the last stage of analysis and visualization, you can do that using code and data provided here. To reproduce everything from volume-level wordcounts, you'll need to unzip [data_for_chapter2.tar.gz](https://www.dropbox.com/s/7oxgti8nofoaiub/data_for_chapter2.tar.gz?dl=0) in chapter2/sourcefiles. To reproduce everything from raw texts, you'll need to contact HathiTrust.

code
----
Code used to produce intermediate data files, not final code for viz. A lot of the work here is done by reproduce.py, which calls code in the top-level /logistic folder to do predictive modeling of genre.

metadata
--------
Lists of volumes used in modeling, but also a detailed summary of genre categories used in the project, **genrecategorieschapter2.docx.**

modeloutput
----------
Files directly produced by code/reproduce.py.

plotdata
--------
Final versions of data to be used in visualization.

rplots
------
Scripts for visualization. If you want to reproduce a particular figure, this may be the place to start.

sourcefiles
-----------
Empty folder. To be filled with files from data_for_chapter2.tar.gz if you want to recreate analyses from raw volume wordcounts. That file is going to be too large to include here and may be linked via Dropbox or figshare.

surprise
--------
Scripts used to find the passages of Babel-17 that were most "surprising" to prewar models of science fiction--or to be more precise, passages where there was greatest difference between the generic predictions of prewar and postwar models. This directory relies on research undertaken for an article written after most of the rest of the book was completed, and the models it uses are not the same models used in the rest of the chapter. To more fully understand this part of the argument, I recommend consulting [the context of another repository.](https://github.com/tedunderwood/measureperspective)
