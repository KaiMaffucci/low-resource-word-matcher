
# Cherokee Testing

## Property-Based Testing

We can pre-calculate the sizes of certain data structures to see whether the program's behavior makes sense. In this case, I manually calculated the size of the `all_morphemes` list, which contains a list of every possible unique "morpheme" (in quotes because I also include spelling variants). I have an assertion in `ngrams.py` to ensure that it matches my pre-calculated estimate, based on the following:

```
standard syllabary => +86
standard standalone consonant sounds => +15
spelling variants (including standalone consonants) 
    dl_ (- tla), k_ (- ka), j_/ch_, gw_/gu_/kw_ => +6+6+14+21 - 1 ("gu" is double-counted because it is a consonant and "g" + "u")
current total: 147
aspirated sounds (note: realistically, morphemes like "hh" don't exist, but they are included) => +147-2-6 (hna does not get a "hhna" and "hna" already counted; so are "h_" sounds)
glottal-initial sounds => *2
total: 572
```

This took an embarrassingly long time to calculate; it was too little too late when I realized I should've just done counters with loops instead of manually calculating everything myself, but at least I'm (pretty) sure now. 

If I continue with this specific version of the program, I will want to calculate whether the size of the custom distances dictionary I generate is correct, and if the dimensions of the similarity matrix match. It may be more worthwhile to explore other NLP methods instead of continuing this specific tactic, though.

In addition, I also verified that the size of `all_morphemes` is the same as the map that maps the index of the morpheme in the list to the morpheme itself, which is critical for vectorization.

## Examples

"Proof by example" is far from foolproof, but it provides insight into how the program is working.

Homophones seem to be working alright; these are supposed to be an exact match, and they are: ``ᏆᎾ	kwana	ᏆᎾ	quana	1.0000``

The singular and plural versions of words are clearly related, as in this example when "a" changes to "di." However, this also demonstrates some of the limitations of this project: the transition from "a" to "di" is related in the Cherokee language, but the distance function here is agnostic to that. ``ᎠᎿᏬ	ahnawo	ᏗᎿᏬ	dihnawo	0.7217``

One of the main experiments with the work on the Cherokee language here is to see how syllabary transliterations fare when measured against their original phonetics. It was able to pick up on that, for example: ``ᎦᏩᏒᎩ	gawhsvgi	ᎦᏩᏒᎩ	gawasvgi	0.8216``
