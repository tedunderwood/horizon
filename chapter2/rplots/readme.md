rplots
=======

Scripts for the final stage of visualization. I'll try to describe how the data used was originally produced.

**C2Fig1detectnewgate.R** produces figure 2.1, using **mungednewgatesensation.csv** in the /plotdata folder, which in turn is produced by **code/mungingthedetectives.py** from a file in /modeloutput that was originally produced by the option "detectnewgatesensation" **code/reproduce.py**.

**C2Fig2SF.R** produces figure 2.2, using a file in /modeloutput that was originally produced by the option "allSF" in **code/reproduce.py**.

**C2Fig3paceofchange.R** produces figure 2.3, using files from /plotdata that were produced by the option "mutualrecognition" in **code/reproduce.py.**
