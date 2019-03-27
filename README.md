# Historical Text Normalization
Compiled tools, datasets, and other resources for historical text normalization.

The resources provided here have originally been used in the following
publications:

+ Marcel Bollmann. 2018. [Normalization of Historical Texts with Neural Network
  Models](http://www.linguistics.rub.de/forschung/arbeitsberichte/22.pdf). *Bochumer
  Linguistische Arbeitsberichte*, 22.

+ Marcel Bollmann. 2019. A Large-Scale Comparison of Historical Text
  Normalization Systems. In *Proceedings of NAACL-HLT 2019.*


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

Norma (and at least one of its dependencies) needs to be compiled manually on
your system before it can be used.  Detailed instructions for this can be found
[in the Norma repository](https://github.com/comphist/norma).

To use Norma, you need to:

1. Prepare a configuration file; you can use the [recommended configuration
   file](/norma.cfg), but should adjust the filenames given inside.

2. Prepare a lexicon of contemporary word forms.  You can use the contemporary
   datasets provided here for this purpose, and create a lexicon file with the
   following command (example given for German):

       norma_lexicon -w datasets/modern/combined.de.uniq -a lexicon.de.fsm -l lexicon.de.sym -c

   Make sure that the names of the lexicon files match what is given in your
   `norma.cfg` before you start training.

Data files for Norma need to be in two-column, tab-separated format.  To train a
new model, use:

    normalize -c norma.cfg -f datasets/historical/german/german-anselm.train.txt -s -t --saveonexit

The names of the saved model files are defined in `norma.cfg`.

Generating normalizations:

```bash
normalize -c norma.cfg -f datasets/historical/german/german-anselm.dev.txt -s > german-anselm.predictions
```

### Using Marian

You need to install the [Marian
framework](https://github.com/marian-nmt/marian-dev) and clone [the
normalization-NMT repository](https://github.com/tanggongbo/normalization-NMT)
on your local machine.  The latter comes with a `train_seq2seq.sh` script that
**needs to be edited** (mainly with respect to paths to Marian and your data
files, but potentially also your GPU memory and device ID) before you can use
it.

Marian requires separate files for source (historical) and target (normalized)
input, and characters need to be separated by whitespace.  This format can be
easily generated as follows:

    scripts/convert_to_charseq.py datasets/historical/german/german-anselm.{train,test,dev}.txt --to preprocessed

This will create the preprocessed input files (named `train.src`, `train.trg`,
etc.) in the `preprocessed/` subdirectory.  Make sure that the respective
variables in `train_seq2seq.sh` point to these files.  Then, training the model
is as simple as navigating to the `normalization-NMT` directory and calling:

    bash train_seq2seq.sh

Generating normalizations is best done by calling `marian-decoder` directly,
like this:

```bash
cat preprocessed/dev.src | $MARIAN_PATH/marian-decoder -c $MODELDIR/model.npz.best-perplexity.npz.decoder.yaml -m $MODELDIR/model.npz.best-perplexity.npz --quiet-translation --device 0 --mini-batch 16 --maxi-batch 100 --maxi-batch-sort src -w 10000 --beam-size 5 | sed 's/ //g' > german-anselm.predictions
```

Marian outputs predictions in the same format as the input files, i.e. with
whitespace-separated characters, which is why we pipe it through `sed 's/ //g'`
to obtain the regular representations.  You can skip this part, of course, but
it's required if you want to use the evaluation scripts supplied here and/or
compare with the other normalization methods.


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


## License

All software (in the `scripts/` directory) is provided under the [MIT
License](scripts/LICENSE).

Licenses for the datasets differ.  The German Anselm data is licensed under [CC
BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).  The German RIDGES
data is licensed under [CC BY
3.0](https://creativecommons.org/licenses/by-sa/3.0/).  The Icelandic data is
licensed under [GNU LGPL v3](https://opensource.org/licenses/LGPL-3.0).  The
Slovene data is licensed under [CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0/).  The other datasets
unfortunately do not indicate a license, but the rights holders have indicated
that the resource is "free" for research purposes.  Please see the READMEs
included in each dataset subdirectory for more details.
