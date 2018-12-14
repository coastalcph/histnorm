# Portuguese normalization dataset

This dataset comes from the [P.S. Post Scriptum](http://ps.clul.ul.pt/index.php)
project.  I only used the manually normalized subset of the full corpus, as
kindly indicated to me by Rita Marquilhas.

To obtain the two-column normalization dataset, I started from the
TEI-compatible XML format as described in the [Userguide for Digital Edition of
Texts in *P.S. Post
Scriptum*](http://ps.clul.ul.pt/files/Manual_PS_english.pdf), and extracted the
normalization from the following attributes (as described on page 84 of the user
guide):

1. `nform`, indicating the "normalized form".
2. If `nform` was not given, I used the `fform` instead, indicating an "expanded
   form (in the case of abbreviations), free form (in the case of contractions)".
3. If both `nform` and `fform` were not given, the token is not normalized,
   i.e. the original form is also considered to be the normalization.

The texts were extracted by century (as given in the corpus metadata), and
train/dev/test splits were created for each century by shuffling the sentences
and performing an 80/10/10 split.  When performing experiments using a single
"Portuguese" dataset, I simply concatenated the respective splits from each
century.
