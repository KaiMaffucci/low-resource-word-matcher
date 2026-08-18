
# NOTE: "nah" syllable is kind of a problem?
def n_gram(A_words, B_words, n=2):

    # generate n-grams for each word in each set
    A_words = tokenize(A_words, n)
    B_words = tokenize(B_words, n)

    # build ngram vocab for vectorization
    
    # build massive list of all morphemes based on my grammar
    """
    GRAMMAR (with or's after each line):
    nah | hna
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
    # add all syllables including standalone consonants/vowels
    # TODO: maybe put this in a function?
    ts_sounds = [morph for morph in all_morphemes if morph[:-1] == "ts"].append("ts")
    j_sounds = [morph for morph in all_morphemes if morph[:-1] == "j"].append("j")
    qu_sounds = [morph for morph in all_morphemes if morph[:-1] == "qu"].append("qu")
    tl_sounds = [morph for morph in all_morphemes if morph[:-1] == "tl"].append("tl")
    dl_sounds = [morph for morph in all_morphemes if morph[:-1] == "dl"].append("dl")
    d_sounds = [morph for morph in all_morphemes if morph[:-1] == "d"].append("d")
    g_sounds = [morph for morph in all_morphemes if morph[:-1] == "g"].append("g")
    k_sounds = [morph for morph in all_morphemes if morph[:-1] == "k"].append("k")
    # NOTE: *not* aspiration (h before consonant). This is for normal h syllables
    h_sounds = [morph for morph in all_morphemes if morph[:-1] == "h"].append("h")
    l_sounds = [morph for morph in all_morphemes if morph[:-1] == "l"].append("l")
    s_sounds = [morph for morph in all_morphemes if morph[:-1] == "s"].append("s")
    m_sounds = [morph for morph in all_morphemes if morph[:-1] == "m"].append("m")
    n_sounds = [morph for morph in all_morphemes if morph[:-1] == "n"].append("n")
    t_sounds = [morph for morph in all_morphemes if morph[:-1] == "t"].append("t")
    w_sounds = [morph for morph in all_morphemes if morph[:-1] == "w"].append("w")
    y_sounds = [morph for morph in all_morphemes if morph[:-1] == "y"].append("y")

    # includes standalone vowels like a (for now)
    a_sounds = [morph for morph in all_morphemes if morph[-1] == "a"]
    e_sounds = [morph for morph in all_morphemes if morph[-1] == "e"]
    i_sounds = [morph for morph in all_morphemes if morph[-1] == "i"]
    o_sounds = [morph for morph in all_morphemes if morph[-1] == "o"]
    u_sounds = [morph for morph in all_morphemes if morph[-1] == "u"]
    v_sounds = [morph for morph in all_morphemes if morph[-1] == "v"]

    # account for custom distances
    """
    1. If two morphemes start with the same consonant sound, they are 50% similar. Same with ending with vowels.
    2. Consonant + vowel morphemes will count as 50% similar to standalone vowels if the vowels match; same logic for standalone consonants.
    3. Consonant sounds ts = ch = j (distance between these is 0)
    4. dl + vowel and tl + vowel should have a 25% difference for matching vowels, and 75% difference for nonmatching vowels, except for dla and tla, which should be 50% similar. Only the Ꮬ and Ꮭ syllables differentiate between dla and tla: all other tl syllables could also be dl.
    5. Aspirated consonants + vowel (eg. hw + vowel) will be considered 75% similar, or aspiration will be on a different axis entirely. h + consonant indicates aspiration, but is left out of syllabary and often left out of phonetics.
    6. g and k (except when in ka) are considered 50% similar as opposed to 0%. This is to account for the syllables Ꭸ, Ꭹ, Ꭺ, Ꭻ, and Ꭼ all being transliterated as g + vowel in my program, even though they can also make the k sound. This needs to be accounted for since there is no prior word tagging.
    """

    # this function returns a dictionary to update the main big dictionary with
    # this is for generic similar sounds, such as syllables with matching consonants or vowels
    def add_dists(sounds1, sounds2=[], dist=0.5):
        new_dists = {}
        if sounds2 == []:
            sounds2 = sounds1
        for s1 in sounds1:
            for s2 in sounds2:
                if s1 != s2:
                    new_dists[frozenset(s1, s2)] = dist
        return new_dists

    # for situations where matching consonant sounds are considered EQUAL, like ts and j
    # sounds1 and sounds2 are expected to be DIFFERENT LISTS
    def add_equ_dists(sounds1, sounds2):
        new_dists = {}
        for s1 in sounds1:
            for s2 in sounds2:
                if s1[-1] == s2[-1]: 
                    new_dist = 0
                else:
                    new_dist = 0.5
                new_dists[frozenset(s1, s2)] = new_dist
        return new_dists
    
    # for situations like tl- and dl- or g- and k- (barring ga/ka)
    # sounds1 and sounds2 are expected to be DIFFERENT LISTS
    def add_semi_dists(sounds1, sounds2):
        new_dists = {}
        for s1 in sounds1:
            for s2 in sounds2:
                # consonants considered automatically half-similar
                if s1[-1] == s2[-1]: 
                    new_dist = 0.25
                else:
                    new_dist = 0.75
                new_dists[frozenset(s1, s2)] = new_dist
        return new_dists

    dist_dict = {}

    # morphemes with shared consonants (including standalone) have 0.5 distance, except dla (has own character in syllabary)
    # this will get some redundant ones like k- and g- that we will fix later
    dist_dict.update(add_dists(ts_sounds))
    dist_dict.update(add_dists(j_sounds))
    dist_dict.update(add_dists(qu_sounds))
    dist_dict.update(add_dists(tl_sounds))
    dist_dict.update(add_dists(d_sounds))
    dist_dict.update(add_dists(dl_sounds))
    dist_dict.update(add_dists(g_sounds))
    dist_dict.update(add_dists(k_sounds))
    dist_dict.update(add_dists(h_sounds))
    dist_dict.update(add_dists(l_sounds))
    dist_dict.update(add_dists(m_sounds))
    dist_dict.update(add_dists(n_sounds))
    dist_dict.update(add_dists(s_sounds))
    dist_dict.update(add_dists(t_sounds))
    dist_dict.update(add_dists(w_sounds))
    dist_dict.update(add_dists(y_sounds))

    # morphemes with shared vowels (including standalone) have 0.5 distance
    dist_dict.update(add_dists(a_sounds))
    dist_dict.update(add_dists(e_sounds))
    dist_dict.update(add_dists(i_sounds))
    dist_dict.update(add_dists(o_sounds))
    dist_dict.update(add_dists(u_sounds))
    dist_dict.update(add_dists(v_sounds))

    # ts = j implies 0 distance (may need to add ch later)
    dist_dict.update(add_equ_dists(ts_sounds, j_sounds))

    # dl + tl (except dla and tla) have 0.25 distance for matching vowel morphemes, nonmatching vowels have 0.75 distance
    dist_dict.update(add_semi_dists(dl_sounds, tl_sounds))
    dist_dict[frozenset("dla", "tla")] = 0.5

    # (h consonant [vowel]) have distance of 0.25 from original matching (consonant vowel)
    # TODO

    # g and k syllables (except in "ka" and "ga" because they have different characters)
    # have 0.25 distance, like dl- and tl-
    dist_dict.update(add_semi_dists(g_sounds, k_sounds))
    dist_dict[frozenset("ga", "ka")] = 0.5

    # test code: print dictionary


    # TODO: save this to a json file and add option for loading it
    # so we don't have to generate all this every time

    # building the distance matrix is going to suck, but it'll work


    # generate a vector for each word's n-gram list


    return A_words, B_words


def tokenize(words, n):

    for w in range(len(words)):
        # crazy freaking trick
        words[w].ngrams = list(zip(*(words[w].morphemes[i:] for i in range(n))))

    return words


def vectorize(words, vocab):
    pass