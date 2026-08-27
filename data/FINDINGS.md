
# Findings, Discussion, Limitations & Conclusion

## What the Program Does Right

As discussed in `TESTING.md`, the program has successfully detected spelling variants and similar words. 

The `results` files include any word matches with a similarity strictly greater than 0.7.

### Examples of Successful Spelling Variant Detection

```
ᏒᎦᏔ	svkta	ᏒᎦᏔ	svgata	0.7939
ᏆᎾ	kwana	ᏆᎾ	quana	1.0000
ᎧᏄᎦᎵ	kanugahli	ᎧᏄᎦᎵ	kanugali	0.9091
ᎦᏩᏒᎩ	gawhsvgi	ᎦᏩᏒᎩ	gawasvgi	0.8216
ᎣᏂᏥ	ontsi	ᎣᏂᏥ	onitsi	0.8660
ᎠᏂ	a'ni	ᎠᏂ	ani	0.9500
ᎢᏤᎢᏳᏍᏗ	ijeiyusdi	ᎢᏤᎢᏳᏍᏗ	itseiyusdi	1.0000
ᏕᎷᎨ	dehluge	ᏕᎷᎨ	deluge	0.8750
```

### Examples of Detecting General Word Similarities

As discussed in `TESTING.md`, it can pick up on singular/plural:

```
ᎠᎿᏬ	ahnawo	ᏗᎿᏬ	dihnawo	0.7217
ᏗᎿᏬ	dihnawo	ᎠᎿᏬ	ahnawo	0.7217
```

It can also detect related words topic-wise. Take the colors, for example:

```
ᎩᎦᎨ	gigage	ᏌᎪᏂᎨ	sagonige	0.8216
ᎠᏓᎶᏂᎨ	adalonige	ᏓᎶᏂᎨ	dalonige	0.9186
ᎠᏓᎶᏂᎨ	adalonige	ᏌᎪᏂᎨ	sagonige	0.7303
ᏓᎶᏂᎨ	dalonige	ᎠᏓᎶᏂᎨ	adalonige	0.9186
ᏓᎶᏂᎨ	dalonige	ᏌᎪᏂᎨ	sagonige	0.7826
ᏌᎪᏂᎨ	sakonige	ᎩᎦᎨ	gigage	0.7217
ᏌᎪᏂᎨ	sakonige	ᎠᏓᎶᏂᎨ	adalonige	0.7217
ᏌᎪᏂᎨ	sakonige	ᏓᎶᏂᎨ	dalonige	0.7660
ᏌᎪᏂᎨ	sakonige	ᏌᎪᏂᎨ	sagonige	0.9487
ᎩᎦᎨ	gigage	ᏌᎪᏂᎨ	sagonige	0.8216
ᎩᎦᎨ	gigage	ᎬᎿᎨ	gvhnage	0.8165
```

## Some Cautions with the Findings

Many matches are seemingly unrelated or coincidental, yielding many false positives. This puts into question the authenticity of the true positives. On the other hand, this may draw new connections between words with similar roots that were not picked up on before. I am extremely far from qualified to make that judgment, though. It may also come down to tweaking how distances/similarities between various morphemes are valued.

```
ᎧᏄᎦᎵ	kanugahli	ᏩᎫᎩ	wagugi	0.7462
ᏆᏁᎾ	quanena	ᏆᎾ	quana	0.9037
ᎧᏄᎦᎵ	kanugahli	ᏩᎫᎩ	wagugi	0.7462
ᎩᏔᏯ	gitaya	ᏒᎦᏔ	svgata	0.7500
ᎩᏔᏯ	gitaya	ᎦᏩᏒᎩ	gawasvgi	0.7144
ᎤᏂᏖᎸᎳᏗ	unitelvladi	ᏓᎶᏂᎨ	dalonige	0.7071
ᎧᏩᏯ	kawaya	ᎠᎿᏬ	ahnawo	0.7144
ᎠᏌᏃ	asano	ᏆᎾ	quana	0.7217
ᎠᏌᏃ	asano	ᎠᏂ	ani	0.7071
ᎠᏌᏃ	asano	ᎠᏓᎶᏂᎨ	adalonige	0.7144
```

To name a few examples.

## Limitations and Next Steps

First, I must address difficulties in attempting n-gram tokenization on Cherokee phonetics. The problem I ran into was that even with only `n=2`, I would end up generating a similarity matrix larger than `60,000 x 60,000`. This, plus the size of the vectorized words themselves, had no hope of fitting in memory even with the most efficient data structures for sparse matrices. Therefore, for now, the Cherokee version only uses "unigrams," measuring the distances between individual morphemes; NOT true grams.

This leads me to a few ideas. My first idea is to construct an on-demand similarity matrix based on the input dataset, instead of trying to account for every possible morpheme. Many morphemes like `'hh` are theoretically possible in Cherokee but practically do not exist. Furthermore, certain properties of morphemes, like aspiration or being glottal-initial, only need a simple 0 or 1, true or false value. Instead of doubling the number of indices in each word vector, one could put properties like these on separate axes. 

In this day and age, most modern NLP is done with machine learning techniques. This is something I am considering myself. However, even if it is not "AI" per se, especially the generative kind pervading the news, many community members are skeptical of feeding their language into anything "AI-shaped" or "AI-like." This comes down to sovereignty. [It can be done well](https://www.npr.org/2026/07/26/nx-s1-5825798/robot-speaks-endangered-native-american-languages), but communities must retain full control over where the data goes. The last thing people want is sensitive cultural data spreading to corporate LLMs that take advantage of the language, culture, and people for their own profit. Once something is out there, it is virtually impossible to take back. These are the main reasons why I have decided to take a rules-based approach to Cherokee NLP, especially since I am acting largely independently and lack credibility.

I hope to eventually write a paper on my project's findings and its limitations, but hopefully this document has proven to be helpful in explaining what is going on in this repository.
