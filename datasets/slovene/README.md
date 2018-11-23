# Slovene normalization dataset

This dataset comes from the [goo300k reference corpus of historical
Slovene](http://nl.ijs.si/imp/index-en.html).  More concretely, it is simply a
processed version of the [KonvNormSl 1.0 dataset of normalised
Slovene](https://www.clarin.si/repository/xmlui/handle/11356/1068) that is made
available under the [CC BY-SA 4.0
license](https://creativecommons.org/licenses/by-sa/4.0/).

The original dataset is in one-token-per-line format with added
beginning-of-word and end-of-work markers, as well as individual characters
separated by spaces.  To keep in line with the format of the other datasets, the
version in this repo "undoes" these preprocessing decisions, but is otherwise
identical to it.
