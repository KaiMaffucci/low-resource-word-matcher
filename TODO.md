# Overall Long-Term Goals

## Near-future

 - **Create base version**. The basic process will consist of uploading two sets of word data (A and B), then comparing each word in set A against set B in a bipartite manner to detect possible word matches. Language-agnostic, which means it may be less effective than catered versions.
 - **Add Cherokee (Tsalagi)-specific functionality.** Details in the Cherokee section of this document.

## Far future

Explore:
 - How machine learning (not necessarily AI) can assist in rule detection. For now, I will likely be sticking mostly to rule-based NLP.
 - Accounting for large datasets, big enough where each dataset cannot fit into standard RAM sizes.
 - Parallel processing for word-matching
 - Comparing transcriptions from TTS applications to written words

# Generalized Version

1. **Load data**. Load data from storage into memory in a structured format, such as lists or dictionaries. Ensure text strings are loaded as Unicode, especially when that may be imperative.
2. **Normalize**. Strip characters of unnecessary elements, such as capitalization, accents, and punctuation. There will be a default normalizer function, but you may specify your own.
3. **Parse**. At this point, we will have text strings each corresponding to one word. The goal here will be to parse each word into morphemes. The default parser will parse each character as a morpheme, but one may pass their own parser. This is important for most languages, as even the presence of a single diphthong could throw the program off.
4. **n-gram tokenization + vectorization**. Builds n-gram tokens for each word out of morphemes. Default n=2.
5. **Cosine similarity**. Performs cosine similarity on the tokenized version of each word in set A against each word in set B in a bipartite manner. 
6. **Output scores**. Outputs the similarity of each word in set A to set B. One parameter will determine at what similarity one chooses to keep or discard a match. For example, a word-to-word similarity of only 20% indicates the words are probably not related. I will have to determine what a logical default percentage will be.

# Cherokee (Tsalagi) Specifications

**DISCLAIMER**: I am not Indigenous, let alone enrolled in a Cherokee nation. While I am taking courses with the Cherokee Nation of OK, take **everything** I say about the Cherokee language with a *huge* grain of salt. If you have questions about the language, it is best to ask a native speaker, or at least a second-language learner enrolled in one of the three federally recognized Cherokee nations (Cherokee Nation OK, United Keetowah Band OK, Eastern Band NC).

1. **Loader.** I will likely start by comparing words from my Cherokee Anki deck as I progress through the Cherokee Nation of Oklahoma's online language courses (1-4). This dataset interests me because I can take the versions of the words written in syllabics, transliterate the syllabics to phonetics, then compare those versions of each word against the phonetics in my original notes. I will explain either here or in the loader file how I will do this, but these details are not as important to the NLP process for now. There is one important note, though: we will want to save the phonetic transliteration that came from what syllabary word originally so that we may compare accuracy. This will add another layer of complexity that I will tackle as I go along.
2. **Normalizer.** Frankly, there's not much to be done here for Cherokee, so I'll probably end up using my default normalizer.
3. **Parser.** This is where we get deep into Cherokee phonetics. I will be counting each Cherokee syllable as a morpheme, with consonant sounds grouped (so *tsa* and *sa* are each one syllable and morpheme). I may explore separating the consonant-vowel pairs from each other, but this is likely what I will try first, as I feel it is more accurate to the structure of the language. Immediately below will be my syntax tree for parsing. It may end up making more sense to split syllables apart. Both strategies may be employed. Another quick note: the glottal stop character ' 

Syntax tree:

WORD: SYLLABLE+

SYLLABLE: h consonant vowel |\
&emsp;&emsp;consonant vowel |\
&emsp;&emsp;vowel |\
&emsp;&emsp;'

4. **n-gram tokenization and vectorization**. Building the n-gram tokens will likely use the default tokenizer, as all we need to do is glue morphemes together according to n. Vectorization will need to take into account certain norms about written Cherokee, listed below. 
 - If two morphemes start with the same consonant sound, they are 50% similar. Same with ending with vowels.
 - Consonant + vowel morphemes will count as 50% similar to standalone vowels if the vowels match.
 - Consonant sounds *ts* = *ch* = *j* (distance between these is 0)
 - *dl* + vowel and *tl* + vowel should have a 25% difference for matching vowels, and 75% difference for nonmatching vowels, except for *dla* and *tla*, which should be 50% similar. Only the Ꮬ and Ꮭ syllables differentiate between *dla* and *tla*: all other *tl* syllables could also be *dl*.
 - Aspirated consonants + vowel (eg. *hw* + vowel), potentially barring *hl* + vowel (due to similarity with *tl* + vowel), will be considered 75% similar, or aspiration will be on a different axis entirely. *h* + consonant indicates aspiration, but is left out of syllabary and often left out of phonetics.
 - *g* and *k* (except when in *ka*) are considered 50% similar as opposed to 0%. This is to account for the syllables Ꭸ, Ꭹ, Ꭺ, Ꭻ, and Ꭼ all being transliterated as *g* + vowel in my program, even though they can also make the *k* sound. This needs to be accounted for since there is no prior word tagging.
 - *qu* + vowel and *gu* + vowel may want to be parsed and weighted equally, since the Ꮖ, Ꮗ, Ꮘ, Ꮙ, Ꮚ, and Ꮛ syllables are sometimes written as *qu* + vowel or *gu* + vowel.
 - *wh* = *wa*. This is a pattern I noticed in a word in the Durbin Feeling online dictionary, but I'm not sure if it'll matter for my datasets.

5. **Cosine similarity**. Now it is a matter of computing cosine similarity between tokens, taking special rules from vectorization into account. 
6. **Output**. This shouldn't be too different, aside from having to account for the original syllabary versions of transliterated words. We want to see how accurate the program is here.
