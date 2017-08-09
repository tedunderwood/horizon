Chapter 1 code
===========

**createcolorfic** produces data used in Figure 1.1.

**createhardaverages** produces data used in Figure 1.2.

**biomodel.py** does predictive modeling of fiction against biography, to produce summaries used in Figures 1.3 and 1.4. Note that there are some loose wires in this code still: paths that will need changing to point to the correct places on your machine.

**inquirer_correlations** correlates **biomodel**'s predictions about volumes with word lists borrowed from the Harvard General Inquirer. Note that the General Inquirer is being used here in a loose way, without some of the contextual subtleties available in the Harvard code itself.

I believe all of these scripts will need the volumes from **data_for_chapter1.tar.gz** unpacked and placed in chapter1/sourcefiles.
