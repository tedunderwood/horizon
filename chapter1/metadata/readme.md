Chapter 1 metadata
==================

Metadata used by various scripts in this chapter.

To fully understand the versioning of different metadata sets, you might want to consult [error/errorinfigs3and4](https://github.com/tedunderwood/horizon/blob/master/chapter1/error/errorinfigs3and4.ipynb). In that notebook I systematically correct errors in the metadata, but preserve the old version so that I can assess the difference that manual cleaning made.

Most volumes in this chapter are dated by **volume publication date**, not by **first publication of the work itself.** This is true even for the column **firstpub** in these metadata files. (Constraints elsewhere in my code have caused me to keep the name **firstpub,** but in this chapter that's a date of volume publication, not first publication of the work.)

Note also that the definitions of "biography" and "fiction" are elucidated in [error/errorinfigs3and4.](https://github.com/tedunderwood/horizon/blob/master/chapter1/error/errorinfigs3and4.ipynb)

**allgenremeta** covers all the volumes in data_for_chapter1.tar.gz, but its genre categories are not fully up to date. Probably should be deprecated.

**oldgenremeta2** is the state of the metadata before error correction.

**hathigenremeta** has gone through one pass of error correction, although it still contains a level of error (as acknowledged in error/errorinfigs3and4.). just contains HathiTrust volumes; this is used by the predictive models that produced figures 1.3 and 1.4.

**eccogenremeta** is only used in error testing; see error/errorinfigs3and4.

**prestigeset** is a subset of volumes categorized by reception, used in fig 1.1.

