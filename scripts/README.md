# Auxiliary scripts for historical text normalization

The scripts in this directory are mostly based on **Python 3.** The required
packages are listed in `requirements.txt` and can be installed via `pip install
-r requirements.txt`.

**As a general rule, all scripts offer the `-h/--help` flag for detailed
instructions on how to use them.**


## General-purpose scripts

- **`preprocess.py`**: Implements all preprocessing steps for historical
  datasets, such as lowercasing, punctuation removal, etc.  To produce the same
  preprocessing as in Bollmann (2019), run the script with the `--all` flag:

      ./preprocess.py --all train.txt

  If you want more fine-grained control, the script also offers plenty of
  command-line options (that you can list via `-h/--help`).

- **`evaluate.py`**: Performs evaluation of word accuracy and character error
  rate, optionally with stemming or restricted to incorrect/seen/unseen tokens.
  For example, to evaluate normalization quality based on word stems on
  out-of-vocabulary tokens only, you could use:

      ./evaluate.py -i --stem english english.test.txt english.pred english.train.txt

- **`significance.py`**: Computes statistical significance of word accuracy
  between two predicted normalizations.

- **`split_sample.py`**: Splits an input file into *n* samples, either randomly
  or in continuous blocks.  Can be used to recreate the training curves found in
  Bollmann (2019); e.g., the following command would produce the ten training
  sets used in the "100 tokens" setting:

      ./split_sample.py -c -n 10 -s 100 english.train.txt english-split

  The last argument specifies a prefix for the output files; the training sets
  in this case would be named `english-split_1`, `english-split_2`, and so on.


## Preprocessing for specific tools

- **`convert_to_charseq.py`**: Converts the two-column, tab-separated format
  found in this repo to separate source/target files with characters separated
  by whitespace.  This is the required input format for XNMT and Marian.

- **`convert_to_orignorm.sh`**: Converts the two-column, tab-separated format
  found in this repo to separate source/target files ending in `.orig` and
  `.norm`.  This is the required input format for the cSMTiser/Moses toolchain.


## Contemporary data

The following scripts were used to extract data from the Europarl v7 corpus:

- **`europarl_extract.py`**: Finds and extracts lines in the Europarl corpus
  that exist in all of the specified languages.

- **`europarl_convert_extracted.bash`**: Utility script to convert the extracted
  excerpts into a full-form wordlist.


## License

All scripts are provided under the [MIT License](LICENSE).
