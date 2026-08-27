
# Cherokee (Tsalagi)-Specific Functionality

## loader.py

`load(fname) -> A_words, B_words`: As discussed in the `README.md`, this program expects one file where each line consists of English words, then Cherokee syllabics, then Cherokee phonetics. This program loads the original dataset into memory for A_words, and for B_words, it transliterates the syllabics into new phonetics based on the generic rules of Cherokee syllabics, with no prior word tagging or anything. Syllabics are stored in `WordObj`'s `raw` attribute, and phonetics in `alt`.

## normalize.py

`normalize(A_words, B_words) -> A_words, B_words`: Removes accents from and lowercases the alt text in each word object it is given. Nothing too fancy going on here.

## parse.py

`parse(A_words, B_words) -> A_words, B_words`: Breaks down each word into individual morphemes and stores them in the `word_list` attribute of each word object. Here is the grammar tree:

```
'nah |
'hna |
'dl VOWEL |
'h CONSONANT VOWEL |
' CONSONANT VOWEL |
' VOWEL |
'h CONSONANT |
' CONSONANT |
's |
nah |
hna |
dl VOWEL |
h CONSONANT VOWEL |
CONSONANT VOWEL |
VOWEL |
h CONSONANT |
CONSONANT |
s
```

## ngram.py



## cosine.py

## output.py

