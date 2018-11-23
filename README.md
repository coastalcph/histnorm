# Historical Text Normalization
Compiled tools, datasets, and other resources for historical text normalization.


## Tools

+ [Norma](https://github.com/comphist/norma), described in [Bollmann
  (2012)](https://marcel.bollmann.me/pub/acrh12.pdf)
+ [Marian (NMT) for normalization](https://github.com/tanggongbo/normalization-NMT),
  described in [Tang et al. (2018)](http://aclweb.org/anthology/C18-1112)
+ [cSMTiser](https://github.com/clarinsi/csmtiser)


## Datasets

Language   | Source Corpus                                                                                                        |  Time Period | Genre            | Tokens (total) | Dataset Location                                          |
----------- | -------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------- | -------------- | ----------------------------------------------------------
English    | [ICAMET](https://www.uibk.ac.at/anglistik/research/projects/icamet/)                                                 |    1386-1698 | Letters          | 188,158        | [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)¹
German     | [RIDGES](https://www.linguistik.hu-berlin.de/en/institut-en/professuren-en/korpuslinguistik/research/ridges-projekt) |    1482-1652 | Science          | 71,570         | [datasets/german/](datasets/german/)
Hungarian  | [HGDS](http://omagyarkorpusz.nytud.hu/en-intro.html)                                                                 |    1440-1541 | Religion         | 172,064        | [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)
Icelandic  | [IcePaHC](http://www.linguist.is/icelandic_treebank/Icelandic_Parsed_Historical_Corpus_(IcePaHC))                    |      15th c. | Religion         | 65,267         | [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)
Portuguese | [Post Scriptum](http://ps.clul.ul.pt/index.php)                                                                      | 15th-19th c. | Letters          | 306,946        | [datasets/portuguese/](datasets/portuguese/)
Slovene    | [goo300k](http://nl.ijs.si/imp/index-en.html)                                                                        |    1750-1899 | Mixed            | 326,538        | [datasets/slovene/](datasets/slovene/)
Spanish    | [Post Scriptum](http://ps.clul.ul.pt/index.php)                                                                      | 15th-19th c. | Letters          | 132,248        | [datasets/spanish/](datasets/spanish/)
Swedish    | [GaW](http://gaw.hist.uu.se)                                                                                         |    1527-1812 | Official Records | 65,571         | [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)

¹Due to licensing restrictions, the ICAMET dataset may not be distributed
further, but the [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)
website contains instructions on how to obtain the same dataset splits.
