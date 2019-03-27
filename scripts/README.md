# Auxiliary scripts for historical text normalization

This directory contains the following general-purpose scripts:

- `preprocess.py`: Implements all preprocessing steps for historical datasets,
  such as lowercasing, punctuation removal, etc.

- `evaluate.py`:
  Performs evaluation of word accuracy and character error rate,
  optionally with stemming or restricted to incorrect/seen/unseen tokens

- `significance.py`:
  Computes statistical significance of word accuracy between two
  predicted normalizations


## Preprocessing for specific tools

- `convert_to_charseq.py`: Converts the two-column, tab-separated format found
  in this repo to separate source/target files with characters separated by
  whitespace.  This is the required input format for XNMT and Marian.

- `convert_to_orignorm.sh`: Converts the two-column, tab-separated format found
  in this repo to separate source/target files ending in `.orig` and `.norm`.
  This is the required input format for the cSMTiser/Moses toolchain.


## Contemporary data

The following scripts were used to extract data from the Europarl v7 corpus:

- `europarl_extract.py`:
  Finds and extracts lines in the Europarl corpus that exist in all of the
  specified languages.

- `europarl_convert_extracted.bash`:
  Utility script to convert the extracted excerpts into a full-form wordlist

## License

All scripts are provided under the [MIT License](LICENSE).
