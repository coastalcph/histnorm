# German normalization dataset

## RIDGES

This dataset comes from Version 5.0 of the [RIDGES (Register in Diachronic
German Science)
project](https://www.linguistik.hu-berlin.de/en/institut-en/professuren-en/korpuslinguistik/research/ridges-projekt).

The two-column normalization dataset was prepared by Uwe Springmann, Bryan
Jurish, and Martin Klotz.  It is comprised of 16 texts from the corpus
originating between 1482 and 1652; newer texts were deliberately included as
they tend to show significantly less variation.  For each text, a random
70/15/15 split of sentences was performed to create the final train/dev/test
splits.


## Anselm

This dataset comes from a preliminary version of the [Anselm
Corpus](https://www.linguistics.rub.de/anselm/access/index.en.html), meaning
that the data found in the released version of the corpus might differ slightly
from that reproduced here.

The dataset is based on 46 texts of the corpus.  For each text, the first 1,000
tokens are used for the dev set, the next 1,000 tokens for the test set, and the
remainder for the training set.  For more detailed information, see [Bollmann,
2018,
Sec. 3.1.2](https://www.linguistics.rub.de/forschung/arbeitsberichte/22.pdf#page=57).
