Chapter Three
============================================

"The Long Arc of Prestige."

figures
-------

**Figure 3.1** is produced by rplots/C3Fig1poetrymodel.R, drawing on a model created by code/reproduce_poetic_prestige.py.

**Figure 3.2** is produced by rplots/C3Fig2fictionmodel.R, drawing on a model created by code/reproduce_fictional_prestige.py.

**Figure 3.3** is produced by salesdata/other_visualizations.ipynb, using data developed by other notebooks in salesdata.

**Figure 3.4** and **Figure 3.5** are both produced by salesvisualizations.ipynb at the top level of the chapter 3 folder, using data developed in the salesdata subfolder.

It's possible that the visualizations currently produced by Jupyter notebooks will need to be replaced by R scripts for consistency across the book.

subdirectories
--------------

**code** contains mostly Python code used to generate models; the output of these processes goes to **modeloutput.**

**metadata** contains lists of volumes used in modeling.

**rplots** contains R scripts used for producing two figures.

Many tests mentioned in passing in the chapter can be reproduced using the Jupyter notebook, **chapter3main.**

But that analysis may depend on a previous set of results produced by a machine learning model. So if you're aiming for complete from-scratch recreation of my results, you might need to run one of the "reproduce" scripts in the **code** folder.

**sourcefiles** is currently empty. But to run the **code/reproduce** scripts, you would need to unpack data_for_chapter3.tar.gz and put the files in **sourcefiles.**