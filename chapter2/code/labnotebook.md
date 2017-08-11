labnotebook
-----------

When I run

    python3 reproduce.py allSF

I get:

(18, 8)
5600 1
Beginning multiprocessing.
Multiprocessing concluded.

True positives 189
True negatives 198
False positives 15
False negatives 24
F1 : 0.906474820143885
0.9084507042253521 0.908450704225
If we divide the dataset with a horizontal line at 0.5, accuracy is:  0.908450704225

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
