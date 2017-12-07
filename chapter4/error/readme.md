error in chapter 4
================

This chapter works with hundreds of thousands of volumes, so error is a trickier problem here than in chapters 2 or 3. But we can still try to assess the level of error, and check whether it's distributed in a way that might have produced the patterns we see in the data.

If you're wondering how one gathers a hundred thousand volumes of fiction in the first place, my process is descibed in [Understanding Genre in a Collection of a Million Volumes](https://figshare.com/articles/Understanding_Genre_in_a_Collection_of_a_Million_Volumes_Interim_Report/1281251)--a grant-funded project from 2014. I specifically recommend section 5 of the report, which includes an assessment of error. The figures on page 36 of the report suggest that I may have missed as much as 17% of the fiction in HathiTrust (in 2014--the library has since expanded). Moreover, roughly 4% of the volumes included in my list of fiction may actually be nonfiction.

If you're wondering how much effect that would have on a predictive model, I would compare [the error notebook from chapter 1,](https://github.com/tedunderwood/horizon/blob/master/chapter1/error/errorinfigs3and4.ipynb) where much higher levels of error turn out to be tolerable.

Inference of gender creates further opportunities for ambiguity and error. In this project, for instance, many of our inferences about gender are based on names and honorifics (Mr, Mrs, Sir, Lady, Baroness, etc). The gendering of a name is a cultural construct; it may vary over time. See, e.g., [Ashley Wilkes.](https://en.wikipedia.org/wiki/Ashley_Wilkes)

Some of the tools we used (i.e., [GenderID.py, by Baird and Blevins](https://github.com/cblevins/Gender-ID-By-Time)) are explicitly designed to reflect historical changes in the gendering of names.

BookNLP, on the other hand, doesn't explicitly compensate for historical change. But David Bamman checked manually to see whether its level of error was varying significantly over time.

![Precision and recall for BookNLP](https://github.com/tedunderwood/character/blob/master/error/50years.jpg)

I don't feel that those variations are likely to explain away the patterns in the data. To double-check this, I also counted pronouns in the Chicago corpus, and compared that trajectory to the number of words BookNLP had assigned to feminine characters.

![Precision and recall for BookNLP](https://github.com/tedunderwood/character/blob/master/error/pronouncheck.jpeg)

The correlation of those two curves is reassuring. (It's not clear why the pronoun ratio is higher; it's possible that women are mentioned in dialogue more than in narration, but there are also lots of other factors that could make the pronoun count misleading.) 

Our methods have other blind spots as well. For instance, BookNLP will not usually see the gender of first-person narrators. If women writers in the 1950s and 60s had been particularly likely to write first-person narrators, who tended to be women, that might explain why fictional women seem to be missing in the period. But in fact, first-person narrators are a pretty small fraction of fictional characters. Moreover, we checked the distribution of first-person pronouns across author gender and date, and find no suspicious signal there.

Finally, the text of the chapter itself explains that we have compared the patterns observed in different samples of the literary past. The sample drawn from HathiTrust was compared, for instance, to a rather different sample at Chicago -- and also to a list of bestselling books.
