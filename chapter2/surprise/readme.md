surprise
========

Scripts that measure the difference between two perspectives at the level of individual words and pages in a novel.

In contrast to some earlier versions, these scripts normalize model coefficients. In place of raw coefficients, we use the coefficient divided by the variance for that word, taken from the standard_scaler used in the model. This is important, because the coefficients otherwise overstate the effect of common words.
