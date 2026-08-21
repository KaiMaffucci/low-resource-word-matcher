
def parse(A_words, B_words):

    import re

    consonants = r"(?:ts|ch|qu|gw|gu|kw|tl|dl|[jgkhlmnstwyd])"
    vowels = r"[aeiouv]"

    # based off my defined grammar (originally in TODO.md)
    grammar_list = [
        r"'nah",
        r"'hna",
        r"'dl" + vowels, # need to put this manually so we don't parse things as ['d', 'le'] for example
        r"'h" + consonants + vowels,
        r"'" + consonants + vowels,
        r"'" + vowels,
        r"'h" + consonants,
        r"'" + consonants,
        r"'s",

        r"nah",
        r"hna",
        r"dl" + vowels, # need to put this manually so we don't parse things as ['d', 'le'] for example
        r"h" + consonants + vowels,
        consonants + vowels,
        vowels,
        r"h" + consonants,
        consonants,
        r"s"
    ]

    # p meaning pattern of course
    # for each pattern in my list, combine them into one giga-pattern
    grammar = re.compile("|".join(f"(?:{p})" for p in grammar_list))

    # perform actual parsing
    def parse_list(words, grammar):
        for i in range(len(words)):
            words[i].morphemes = grammar.findall(words[i].normal)
        return words
    A_words = parse_list(A_words, grammar)
    B_words = parse_list(B_words, grammar)

    """
    TODO: testing
    put words back together from parsed list,
    save normalized word and new word,
    so test program can detect if any words were not able to be put back together.
    it looks good for now, so I will save this for later
    """

    return A_words, B_words