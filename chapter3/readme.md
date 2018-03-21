Chapter Three
============================================

"The Long Arc of Prestige."

In order to run the **reproduce** scripts in chapter3/code, you would first need to unzip [data_for_chapter3.tar.gz](https://www.dropbox.com/s/urlo2292g3ueozl/data_for_chapter3.tar.gz?dl=0) and use that data to replace the chapter3/sourcefiles folder.

notebooks
---------
Some of the reasoning in this chapter--especially tables 3.2 and 3.3--may be easiest to follow in these Jupyter notebooks. For a richer account of the process that produced sales estimates, see other Jupyter notebooks in the **salesdata** subfolder.

error
-----
There is no separate **error** folder in this chapter, but I recommend consulting the comparisons between differently-balanced models at the end of [notebooks/chapter3main.ipynb,](https://github.com/tedunderwood/horizon/blob/master/chapter3/notebooks/chapter3main.ipynb) and/or the reasoning about missing data in [salesdata/empiricalbayessales.ipynb](https://github.com/tedunderwood/horizon/blob/master/chapter3/salesdata/empiricalbayessales.ipynb).

figures
-------

**Figure 3.1** is produced by rplots/C3Fig1poetrymodel.R, drawing on a model created by code/reproduce_poetic_prestige.py.

**Figure 3.2** is produced by rplots/C3Fig2fictionmodel.R, drawing on a model created by code/reproduce_fictional_prestige.py.

**Figure 3.3** is produced by rplots/C3Fig3salesratio.R, using data produced by salesdata/other_visualizations.ipynb, which in turn uses authordata.csv, produced by salesdata/empiricalbayessales.ipynb.

**Figure 3.4** is produced by rplots/C3Fig4victorianfield.R, using pairedwithprestige.csv, produced by salesdata/empiricalbayessales.ipynb.

**Figure 3.5** is produced by rplots/C3Fig5modernfield.R, using pairedwithprestige.csv, produced by salesdata/empiricalbayessales.ipynb.

subdirectories
--------------

**code** contains mostly Python code used to generate models; the output of these processes goes to **modeloutput.**

**metadata** contains lists of volumes used in modeling.

**rplots** contains R scripts used for producing two figures.

Many tests mentioned in passing in the chapter can be reproduced using the Jupyter notebook, **chapter3main.**

But that analysis may depend on a previous set of results produced by a machine learning model. So if you're aiming for complete from-scratch recreation of my results, you might need to run one of the "reproduce" scripts in the **code** folder.

**sourcefiles** is currently empty. But to run the **code/reproduce** scripts, you would need to unpack [data_for_chapter3.tar.gz](https://www.dropbox.com/s/urlo2292g3ueozl/data_for_chapter3.tar.gz?dl=0) and put the files in chapter3/sourcefiles.
