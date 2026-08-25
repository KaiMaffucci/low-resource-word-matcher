
# Cherokee Testing

# Property-Based Testing

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

