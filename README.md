# Historical Text Normalization
Compiled tools, datasets, and other resources for historical text normalization.

The resources provided here have originally been used in the following
publications:

+ Marcel Bollmann. 2018. [Normalization of Historical Texts with Neural Network
  Models](http://www.linguistics.rub.de/forschung/arbeitsberichte/22.pdf). *Bochumer
  Linguistische Arbeitsberichte*, 22.

+ Marcel Bollmann. 2019 (to appear). A Large-Scale Comparison of Historical Text
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


## Helpful Scripts

The [`scripts/`](scripts/) directory contains a collection of scripts that was
used in the process of running the normalization experiments in Bollmann (2019).
This includes **preprocessing** scripts, **evaluation** and **significance
testing** scripts, and more.  For more details, please see the [README file in
the scripts/ folder](scripts/README.md).


## Tools

The following tools are evaluated in Bollmann (2019):

+ [Norma](https://github.com/comphist/norma), described in [Bollmann
  (2012)](https://marcel.bollmann.me/pub/acrh12.pdf)
+ [Marian (NMT) for normalization](https://github.com/tanggongbo/normalization-NMT),
  described in [Tang et al. (2018)](http://aclweb.org/anthology/C18-1112)
+ [XNMT](https://github.com/neulab/xnmt), following the model of [Bollmann
  (2018)](http://www.linguistics.rub.de/forschung/arbeitsberichte/22.pdf)
+ [cSMTiser](https://github.com/clarinsi/csmtiser) (wrapping Moses)

The detailed instructions below assume that the data files are provided in the
same format as contained in this repository; i.e., as tab-separated text files
where the first column contains a historical word form and the second column
contains its normalization.

### Using Norma

Norma (and at least one of its dependencies) needs to be compiled manually on
your system before it can be used.  Detailed instructions for this can be found
[in the Norma repository](https://github.com/comphist/norma).

To use Norma, you need to:

1. **Prepare a configuration file;** you can use the [recommended configuration
   file](examples/norma.cfg), but should adjust the filenames given inside.

2. **Prepare a lexicon of contemporary word forms.** You can use the
   contemporary datasets provided here for this purpose, and create a lexicon
   file with the following command (example given for German):

       norma_lexicon -w datasets/modern/combined.de.uniq -a lexicon.de.fsm -l lexicon.de.sym -c

   Make sure that the names of the lexicon files match what is given in your
   `norma.cfg` before you start training.

Data files for Norma need to be in two-column, tab-separated format.  To **train
a new model,** use:

    normalize -c norma.cfg -f datasets/historical/german/german-anselm.train.txt -s -t --saveonexit

The names of the saved model files are defined in `norma.cfg`.  **Generating
normalizations** is done via:

```bash
normalize -c norma.cfg -f datasets/historical/german/german-anselm.dev.txt -s > german-anselm.predictions
```

### Using Marian

You need to install the [Marian
framework](https://github.com/marian-nmt/marian-dev) and clone [the
normalization-NMT repository](https://github.com/tanggongbo/normalization-NMT)
on your local machine.  You then need to:

1. **Preprocess the input** to be in separate source/target files with
   whitespace-separated characters.  This format can be easily generated as
   follows:

   ```bash
   mkdir preprocessed
   scripts/convert_to_charseq.py datasets/historical/german/german-anselm.{train,test,dev}.txt --to preprocessed
   ```

   This will create the preprocessed input files (named `train.src`,
   `train.trg`, etc.) in the `preprocessed/` subdirectory.

2. **Edit the `train_seq2seq.sh` script** that comes with normalization-NMT to
   point to the correct paths (for Marian and the preprocessed input), as well
   as adjust the GPU memory settings and device ID to the correct values for
   your system.  As an example, check out [the modified script used for the
   experiments in Bollmann (2019)](examples/train_seq2seq.sh).

Then, **training the model** is as simple as calling:

    bash train_seq2seq.sh

**Generating normalizations** is best done by calling `marian-decoder` directly,
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

XNMT is based on Python 3.6 and DyNet.  You can find detailed instructions on
how to install it [in the "Getting Started" section of the
documentation](https://xnmt.readthedocs.io/en/latest/getting_started.html).

Since XNMT is new software that is changing quickly, and there was no tagged
release at the time of my experiments, **it is possible that the newest version
is not compatible with the exact scripts and instructions provided here.** For
reference, the experiments performed in Bollmann (2019) are based on [XNMT
commit
6557ee8](https://github.com/neulab/xnmt/tree/6557ee8ef8e39a8936035d8aa9ae1c8576d3734d).
You can obtain this exact version of the code by cloning the XNMT repository and
then issuing `git checkout 6557ee8`.

To use XNMT, you need to:

1. **Preprocess the input** to be in separate source/target files with
   whitespace-separated characters (the same as for Marian):

   ```bash
   scripts/convert_to_charseq.py datasets/historical/german/german-anselm.{train,test,dev}.txt --to preprocessed
   ```

2. **Edit [the example configuration file](examples/xnmt-config.yaml)** by
   replacing the `<<TMPDIR>>` string with the path to your preprocessed input
   files; for example:

   ```bash
   sed -i 's|<<TMPDIR>>|./preprocessed|g' examples/xnmt-config.yaml
   ```

   For very small datasets, you might also want to increase the patience value
   (find the line that says `patience: 5` and adjust it).

Afterwards, you can **train the model** by calling:

    PYTHONHASHSEED=0 python3 -m xnmt.xnmt_run_experiments xnmt-config.yaml --dynet-seed 0 --dynet--gpu

This both trains and evaluates; the final predictions will be stored as
`dev.predictions` in the given directory.


### Using cSMTiser

cSMTiser requires an installation of Moses and MGIZA.  Detailed instructions can
be found [in the cSMTiser repository](https://github.com/clarinsi/csmtiser).  To
use it, you need to:

1. **Preprocess the input** to be in separate orig/norm files.  There is a bash
   script to achieve this that has the same argument structure as the script for
   XNMT and Marian above:

   ```bash
   mkdir preprocessed
   scripts/convert_to_orignorm.sh datasets/historical/german/german-anselm.{train,test,dev}.txt --to preprocessed
   ```

2. **Edit [the example configuration file](examples/csmtiser-config.yaml)** by
   replacing the `<<TMPDIR>>` string with the path to your preprocessed input
   files; for example:

   ```bash
   sed -i 's|<<TMPDIR>>|preprocessed|g' examples/csmtiser-config.yaml
   ```

   Likewise, you should replace `<<MODELDIR>>` with the desired output directory
   (absolute path!) for your trained model, and `<<MOSESDIR>>` with the path to
   your local Moses installation.

   To **add the contemporary data for language modelling** (optional), find the
   line in the configuration file that says `lms: []` and replace it with (e.g.)
   `lms: [datasets/modern/combined.de.uniq]`.

Afterwards, **training the model** requires the following two commands (from the
cSMTiser directory):

```bash
python preprocess.py csmtiser-config.yaml
python train.py csmtiser-config.yaml
```

**Generating normalizations** is achieved by calling:

```bash
python normalise.py csmtiser-config.yaml preprocessed/test.orig
```

The predicted normalizations will, in this case, be written to
`preprocessed/test.orig.norm`.


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

## Contact

For questions or problems, feel free to file a GitHub issue, or contact me
directly:

+ Marcel Bollmann (<marcel@bollmann.me>)
