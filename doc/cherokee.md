
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

This is where things start to get complicated.

`n_gram(A_words, B_words) -> A_words, B_words, S`: The central function that generates a similarity matrix and vectorizes each word. It relies on several other helper functions, described below.

`build_dist_dict() -> all_morphemes, dist_dict`: a big, ugly function that generates a dictionary of all the custom distances between individual morphemes, and a list of all the morphemes. The custom distance rules are described below, in no particular order:

 - Generally speaking, if two morphemes start with the same consonant sound, they are 50% similar. Same with ending with vowels.
 - Consonant + vowel morphemes will count as 50% similar to standalone vowels if the vowels match; same logic for standalone consonants.
 - Consonant sounds *ts* = *ch* = *j* (distance is 0)
 - *dl* + vowel and *tl* + vowel should have a 25% difference for matching vowels, and 75% difference for nonmatching vowels, except for *dla* and *tla*, which should be 50% different. Only the Ꮬ and Ꮭ syllables differentiate between *dla* and *tla*: all other *tl* syllables could also be *dl*.
 - Aspirated morphemes are considered 25% different. *h* + morpheme indicates aspiration, but is left out of syllabics and often left out of phonetics. The same principle applies for glottal-initial morphemes.
 - *g* and *k* (except when in *ka*) are considered 50% similar as opposed to 0%. This is to account for the syllables Ꭸ, Ꭹ, Ꭺ, Ꭻ, and Ꭼ all being transliterated as *g* + vowel in my program, even though they can also make the *k* sound. This needs to be accounted for since there is no prior word tagging.
 - *qu* + vowel and *gu*/*gw*/*kw* + vowel are considered equal, since the Ꮖ, Ꮗ, Ꮘ, Ꮙ, Ꮚ, and Ꮛ syllables are sometimes written as *qu* + vowel or *gu* + vowel.
 - *t* + vowel sounds that do not have their own syllabary symbol are considered 25% different for matching vowels and 75% different for nonmatching vowels.

Feel free to inform me if I forgot anything. This function can probably be made slightly less ugly by using regex, but I started doing it the way it is now and stuck with it.

`vectorize(words, index_map) -> words`: takes in a list of word objects and generates word vectors for each word (stored in the `vec` attribute) based on the index map.

`build_unigram_matrix(index_map, dist_dict) -> S`: generates a similarity matrix for later soft cosine similarity calculations.

## cosine.py

`cosine(A_words, B_words, S_matrix) -> G`: performs soft cosine similarity between the vectors of two sets of words based on the similarity matrix `S_matrix`, returning a bipartite graph `G` where the weights on each edge are the distances between the words. The *original* source for soft cosine and for constructing the similarity matrix comes from [this paper](https://www.researchgate.net/publication/267211399_Soft_Similarity_and_Soft_Cosine_Measure_Similarity_of_Features_in_Vector_Space_Model
). 

## output.py

`output(G, threshold_exclusive, outmethod) -> None`: takes in the final graph `G` and asks for additional information on what results are saved and how.
