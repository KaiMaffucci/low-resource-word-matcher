
#from shared.wordobj import WordObj

def n_gram(A_words, B_words, n=2):

    # generate n-grams for each word in each set
    A_words = tokenize(A_words, n)
    B_words = tokenize(B_words, n)

    # build ngram vocab for vectorization
    # account for custom distances


    # generate a vector for each word's n-gram list

    """
    1. If two morphemes start with the same consonant sound, they are 50% similar. Same with ending with vowels.
    2. Consonant + vowel morphemes will count as 50% similar to standalone vowels if the vowels match; same logic for standalone consonants.
    3. Consonant sounds ts = ch = j (distance between these is 0)
    4. dl + vowel and tl + vowel should have a 25% difference for matching vowels, and 75% difference for nonmatching vowels, except for dla and tla, which should be 50% similar. Only the Ꮬ and Ꮭ syllables differentiate between dla and tla: all other tl syllables could also be dl.
    5. Aspirated consonants + vowel (eg. hw + vowel), potentially barring hl + vowel (due to similarity with tl + vowel), will be considered 75% similar, or aspiration will be on a different axis entirely. h + consonant indicates aspiration, but is left out of syllabary and often left out of phonetics.
    6. g and k (except when in ka) are considered 50% similar as opposed to 0%. This is to account for the syllables Ꭸ, Ꭹ, Ꭺ, Ꭻ, and Ꭼ all being transliterated as g + vowel in my program, even though they can also make the k sound. This needs to be accounted for since there is no prior word tagging.
    """

    # building the distance matrix is going to suck, but it'll work
    import numpy as np
    #distance_dict = {}

    # build massive list of all morphemes based on my grammar
    """
    GRAMMAR (with or's after each line):
    nah | hna | dla
    h consonant vowel
    consonant vowel
    ' vowel
    vowel
    h consonant
    consonant
    """
    # set to force uniqueness
    all_morphemes = set()

    consonants = ["ts", "j", "qu", "tl", "d", "dl", "g", "k", "h", "l", "m", "n", "s", "t", "w", "y"]
    vowels = ["a", "e", "i", "o", "u", "v"]

    all_morphemes.add("nah")
    all_morphemes.add("hna")
    all_morphemes.add("dla")
    h = "h" # makes life slightly easier
    for c in consonants:
        all_morphemes.add(c)
        all_morphemes.add(h + c)
        for v in vowels:
            all_morphemes.add(h + c + v)
            all_morphemes.add(c + v)
    for v in vowels:
        all_morphemes.add(v)
        all_morphemes.add("'" + v)
    all_morphemes.add("s")

    # make it a list so it's easier to iterate
    all_morphemes = list(all_morphemes)

    # generate lists for custom distance rules
    # note: are these even necessary? I'm gonna sleep on it and revisit it tomorrow
    ts_sounds = [morph for morph in all_morphemes if morph[:-1] == "ts"]
    j_sounds = [morph for morph in all_morphemes if morph[:-1] == "j"]
    qu_sounds = [morph for morph in all_morphemes if morph[:-1] == "qu"]
    tl_sounds = [morph for morph in all_morphemes if morph[:-1] == "tl"]
    dl_sounds = [morph for morph in all_morphemes if morph[:-1] == "dl"]
    d_sounds = [morph for morph in all_morphemes if morph[:-1] == "d"]
    g_sounds = [morph for morph in all_morphemes if morph[:-1] == "g"]
    k_sounds = [morph for morph in all_morphemes if morph[:-1] == "k"]
    # NOTE: *not* aspiration (h before consonant). This is for normal h syllables
    h_sounds = [morph for morph in all_morphemes if morph[:-1] == "h"]
    l_sounds = [morph for morph in all_morphemes if morph[:-1] == "l"]







    a_sounds = []
    e_sounds = []
    o_sounds = []
    """
    for m in all_morphemes:
        if m[:-1] == "d":
            d_sounds.append()
    """




    return A_words, B_words


def tokenize(words, n):

    for w in range(len(words)):
        # crazy freaking trick
        words[w].ngrams = list(zip(*(words[w].morphemes[i:] for i in range(n))))

    return words


def vectorize(words, vocab):
    pass