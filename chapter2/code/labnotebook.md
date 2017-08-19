labnotebook
-----------

When I run

    python3 reproduce.py allSF

I get:

(21, 3)
4100 0.006
Beginning multiprocessing.
Multiprocessing concluded.

True positives 186
True negatives 200
False positives 13
False negatives 27
F1 : 0.9029126213592233
0.9061032863849765 0.906103286385
If we divide the dataset with a horizontal line at 0.5, accuracy is:  0.906103286385

When I run

    python3 reproduce.py detectnewgatesensation

I get:

(15, 3)
4300 0.006
Beginning multiprocessing.
Multiprocessing concluded.

True positives 258
True negatives 267
False positives 20
False negatives 29
F1 : 0.9132743362831858
0.9146341463414634 0.914634146341
If we divide the dataset with a horizontal line at 0.5, accuracy is:  0.914634146341
