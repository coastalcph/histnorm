# Historical Text Normalization
Compiled tools, datasets, and other resources for historical text normalization.


## Datasets

Language   | Source Corpus                                                                                                        |  Time Period | Genre            | Tokens (total) | Source of Splits                                          |
----------- | -------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------- | -------------- | ----------------------------------------------------------
English¹    | [ICAMET](https://www.uibk.ac.at/anglistik/research/projects/icamet/)                                                 |    1386-1698 | Letters          | 188,158        | [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)
German     | [Anselm](https://www.linguistics.rub.de/anselm/)                                                                     | 14th-16th c. | Religion         | 71,570         | prev. unpublished
German     | [RIDGES](https://www.linguistik.hu-berlin.de/en/institut-en/professuren-en/korpuslinguistik/research/ridges-projekt) |    1482-1652 | Science          | 71,570         | prev. unpublished
Hungarian  | [HGDS](http://omagyarkorpusz.nytud.hu/en-intro.html)                                                                 |    1440-1541 | Religion         | 172,064        | [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)
Icelandic  | [IcePaHC](http://www.linguist.is/icelandic_treebank/Icelandic_Parsed_Historical_Corpus_(IcePaHC))                    |      15th c. | Religion         | 65,267         | [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)
Portuguese | [Post Scriptum](http://ps.clul.ul.pt/index.php)                                                                      | 15th-19th c. | Letters          | 306,946        | prev. unpublished
Slovene    | [goo300k](http://nl.ijs.si/imp/index-en.html)                                                                        |    1750-1899 | Mixed            | 326,538        | [KonvNormSl 1.0](https://www.clarin.si/repository/xmlui/handle/11356/1068)
Spanish    | [Post Scriptum](http://ps.clul.ul.pt/index.php)                                                                      | 15th-19th c. | Letters          | 132,248        | prev. unpublished
Swedish    | [GaW](http://gaw.hist.uu.se)                                                                                         |    1527-1812 | Official Records | 65,571         | [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)

¹Due to licensing restrictions, the ICAMET dataset may not be distributed
further, but the [HistCorp](http://stp.lingfil.uu.se/histcorp/tools.html)
website contains instructions on how to obtain the same dataset splits.


## Tools

+ [Norma](https://github.com/comphist/norma), described in [Bollmann
  (2012)](https://marcel.bollmann.me/pub/acrh12.pdf)
+ [Marian (NMT) for normalization](https://github.com/tanggongbo/normalization-NMT),
  described in [Tang et al. (2018)](http://aclweb.org/anthology/C18-1112)
+ [XNMT](https://github.com/neulab/xnmt), following the model of [Bollmann
  (2018)](http://www.linguistics.rub.de/forschung/arbeitsberichte/22.pdf)
+ [cSMTiser](https://github.com/clarinsi/csmtiser) (wrapping Moses)

The following instructions assume that the data files are provided in the same
format as contained in this repository; i.e., as tab-separated text files where
the first column contains a historical word form and the second column contains
its normalization.

### Using Norma

**TODO: Installation**

**TODO: Provide config file**

Generating a lexicon file:

    norma_lexicon -w <wordlist> -a lexicon.fst -l lexicon.sym -c

Training:

    normalize -c <configfile> -f <trainfile> -s -t --saveonexit

Generating normalizations:

    normalize -c <configfile> -f <evalfile> -s > <predictions>


### Using Marian

**TODO: Installation**

**TODO: customize train_seq2seq.sh**

Training:

    bash train_seq2seq.sh

Generating normalizations:

    cut -f1 <evalfile> | <path-to-marian>/marian-decoder -c <modeldir>/model.npz.best-perplexity.npz.decoder.yaml -m <modeldir>/model.npz.best-perplexity.npz --quiet-translation --device 0 --mini-batch 16 --maxi-batch 100 --maxi-batch-sort src -w 10000 --beam-size 5 | sed 's/ //g' > <predictions>


### Using XNMT

**TODO: Installation**

**TODO: provide config file**

commit 6557ee8ef8e39a8936035d8aa9ae1c8576d3734d

Training:

    PYTHONHASHSEED=0 python3 -m xnmt.xnmt_run_experiments <configfile> --dynet-seed 0 --dynet--gpu

(dev predictions during training are saved in `full_dev.norm`)

Can you even generate normalizations otherwise??


### Using cSMTiser

**TODO: Installation**

*Training used to be kind of awkward; required changing values in a Python
script before calling a series of commands, but I think recent cSMTiser version
changed that.  Check with newest cSMTiser; older scripts are in `_dump` folder*
