
# TODO: flag any words missing the original phonetics

def load(fname = input("Enter file name and path (my Anki deck): ")):

    # regular expressions are super useful here, I'm not sure how I would do this without
    import re
    # for my WordObj class
    from shared.wordobj import WordObj

    # English definition with whitespace, followed by Cherokee syllabary (using Unicode), followed by Cherokee phonetics 
    # this is ugly as heck but it works well enough
    pattern = re.compile(
        r'^([A-Za-z\s,]*?)([\u13A0-\u13FF\uAB70-\uABBF\s,]*?)([A-Za-z\s,]*)$'
    )

    """
    where the syllabry spellings will go (later transliterated into phonetics)
    raw text: syllabics
    alt text: empty for now, will be transliterated into phonetics later
    """
    A_words = []
    """where the original phonetic spellings will go (unchanged)
    raw  text: syllabics
    alt text: original phonetic spelling
    """
    B_words = []

    # have to open it wth utf-8 for Cherokee unicode
    with open(fname, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            match = pattern.match(line)

            if match:
                # _ was original English translation
                _, syllabics, phonetics = match.groups()
                # strip whitespace from end of syllabics and phonetics
                syllabics = syllabics.strip()
                phonetics = phonetics.strip()

                # if the syllabics has only one word, add it to word lists
                if len(syllabics.split()) == 1:
                    A_words.append(WordObj(syllabics))
                    B_words.append(WordObj(syllabics, phonetics))

    # all said and done, print (test code)
    for i in range(len(A_words)):
        print(i)
        print(f"{A_words[i].raw}\t{A_words[i].alt}")
        print(f"{B_words[i].raw}\t{B_words[i].alt}")

    return A_words, B_words