
# TODO: flag any words missing the original phonetics

def load(fname = input("Enter file name and path: ")):

    # regular expressions are super useful here, I'm not sure how I would do this without
    import re
    # for my WordObj class
    from shared.wordobj import WordObj

    # English definition with whitespace, followed by Cherokee syllabary (using Unicode), followed by Cherokee phonetics 
    # this is ugly as heck but it works well enough
    pattern = re.compile(
        r'^([A-Za-z\s,\'’‘]*?)([\u13A0-\u13FF\uAB70-\uABBF\s,]*?)([A-Za-z\s,\'’‘]*)$'
    )

    """where the original phonetic spellings will go (control)
    raw  text: syllabics
    alt text: original phonetic spelling
    """
    A_words = []
    """
    where the syllabry spellings will go (test, later transliterated into phonetics)
    raw text: syllabics
    alt text: empty for now, will be transliterated into phonetics later
    """
    B_words = []

    # have to open it wth utf-8 for Cherokee unicode
    with open(fname, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            # remove text in paretheses
            # this causes vowels to drop, really testing the program's NLP capabilities
            line = re.sub(r'\(.*?\)', '', line)

            match = pattern.match(line)

            if match:
                # _ was original English translation
                _, syllabics, phonetics = match.groups()
                # strip whitespace from end of syllabics and phonetics
                syllabics = syllabics.strip()
                phonetics = phonetics.strip()

                # if the syllabics has only one word, add it to word lists
                if len(syllabics.split()) == 1:
                    A_words.append(WordObj(syllabics, phonetics))
                    B_words.append(WordObj(syllabics))

    # dictionary for transliterating syllabics into phonetics for test word list
    # note: may move this to a json file at some point
    translit_dict = {
        # standalone vowels
        "Ꭰ": "a", "Ꭱ": "e", "Ꭲ": "i", "Ꭳ": "o", "Ꭴ": "u", "Ꭵ": "v",
        # G / K
        "Ꭶ": "ga", "Ꭷ": "ka", "Ꭸ": "ge", "Ꭹ": "gi", "Ꭺ": "go", "Ꭻ": "gu", "Ꭼ": "gv",
        # H
        "Ꭽ": "ha", "Ꭾ": "he", "Ꭿ": "hi", "Ꮀ": "ho", "Ꮁ": "hu", "Ꮂ": "hv",
        # L
        "Ꮃ": "la", "Ꮄ": "le", "Ꮅ": "li", "Ꮆ": "lo", "Ꮇ": "lu", "Ꮈ": "lv",
        # M
        "Ꮉ": "ma", "Ꮊ": "me", "Ꮋ": "mi", "Ꮌ": "mo", "Ꮍ": "mu", "Ᏽ": "mv",
        # N
        "Ꮎ": "na", "Ꮏ": "hna", "Ꮑ": "ne", "Ꮐ": "nah", "Ꮒ": "ni", "Ꮓ": "no", "Ꮔ": "nu", "Ꮕ": "nv",
        # QU
        "Ꮖ": "qua", "Ꮗ": "que", "Ꮘ": "qui", "Ꮙ": "quo", "Ꮚ": "quu", "Ꮛ": "quv",
        # S
        "Ꮝ": "s", "Ꮜ": "sa", "Ꮞ": "se", "Ꮟ": "si", "Ꮠ": "so", "Ꮡ": "su", "Ꮢ": "sv",
        # T / D
        "Ꮣ": "da", "Ꮤ": "ta", "Ꮥ": "de", "Ꮦ": "te", "Ꮧ": "di", "Ꮨ": "ti", "Ꮩ": "do", "Ꮪ": "du", "Ꮫ": "dv",
        # TL/DL
        "Ꮬ": "dla", "Ꮭ": "tla", "Ꮮ": "tle", "Ꮯ": "tli", "Ꮰ": "tlo", "Ꮱ": "tlu", "Ꮲ": "tlv",
        # TS (J)
        "Ꮳ": "tsa", "Ꮴ": "tse", "Ꮵ": "tsi", "Ꮶ": "tso", "Ꮷ": "tsu", "Ꮸ": "tsv",
        # W
        "Ꮹ": "wa", "Ꮺ": "we", "Ꮻ": "wi", "Ꮼ": "wo", "Ꮽ": "wu", "Ꮾ": "wv",
        # Y
        "Ꮿ": "ya", "ye": "ye", "Ᏹ": "yi", "Ᏺ": "yo", "Ᏻ": "yu", "Ᏼ": "yv"
    }

    # perform actual transliteration
    for word in B_words:
        new_word = ""
        for syllable in word.raw:
            s = translit_dict.get(syllable, syllable)
            new_word += s
        word.alt = new_word

    return A_words, B_words