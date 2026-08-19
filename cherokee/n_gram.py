
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
    # TODO: maybe put this in a function? also maybe use regex instead of this way?
    ts_sounds = [m for m in all_morphemes if m[:-1] == "ts"] + ["ts"]
    j_sounds = [m for m in all_morphemes if m[:-1] == "j"] + ["j"]
    qu_sounds = [m for m in all_morphemes if m[:-1] == "qu"] + ["qu"]
    tl_sounds = [m for m in all_morphemes if m[:-1] == "tl"] + ["tl"]
    dl_sounds = [m for m in all_morphemes if m[:-1] == "dl"] + ["dl"]
    d_sounds = [m for m in all_morphemes if m[:-1] == "d"] + ["d"]
    g_sounds = [m for m in all_morphemes if m[:-1] == "g"] + ["g"]
    k_sounds = [m for m in all_morphemes if m[:-1] == "k"] + ["k"]
    # NOTE: *not* aspiration (h before consonant). This is for normal h syllables
    h_sounds = [m for m in all_morphemes if m[:-1] == "h"] + ["h"]
    l_sounds = [m for m in all_morphemes if m[:-1] == "l"] + ["l"]
    s_sounds = [m for m in all_morphemes if m[:-1] == "s"] + ["s"]
    m_sounds = [m for m in all_morphemes if m[:-1] == "m"] + ["m"]
    n_sounds = [m for m in all_morphemes if m[:-1] == "n"] + ["n"]
    t_sounds = [m for m in all_morphemes if m[:-1] == "t"] + ["t"]
    w_sounds = [m for m in all_morphemes if m[:-1] == "w"] + ["w"]
    y_sounds = [m for m in all_morphemes if m[:-1] == "y"] + ["y"]

    # includes standalone vowels like a (for now)
    a_sounds = [m for m in all_morphemes if m[-1] == "a"]
    e_sounds = [m for m in all_morphemes if m[-1] == "e"]
    i_sounds = [m for m in all_morphemes if m[-1] == "i"]
    o_sounds = [m for m in all_morphemes if m[-1] == "o"]
    u_sounds = [m for m in all_morphemes if m[-1] == "u"]
    v_sounds = [m for m in all_morphemes if m[-1] == "v"]

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
                    new_dists[frozenset([s1, s2])] = dist
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
                new_dists[frozenset([s1, s2])] = new_dist
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
                new_dists[frozenset([s1, s2])] = new_dist
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
    dist_dict[frozenset(["dla", "tla"])] = 0.5

    # build list of aspirated morphemes
    aspirated_morphemes = [m for m in all_morphemes if m[0] == 'h' and m not in h_sounds and m != 'hna']
    # (h consonant [vowel]) have distance of 0.25 from original matching (consonant vowel)
    # TODO: put in own function for cleanliness? 
    for a in aspirated_morphemes:
        # list comprehension includes
        for m in all_morphemes:
            new_dist = 0
            if a != m:
                # normal h sounds
                if m in h_sounds:
                    # if vowels match
                    if a[-1] == m[-1]:
                        dist_dict[frozenset([a, m])] = 0.5
                        continue # yeah
                                    
                # if aspirated consonant in a == consonant in m
                if a[1:-1] == m[:-1]:
                    new_dist += 0.25
                else:
                    new_dist += 0.5
                # if vowels don't match, increase distance
                if a[-1] != m[-1]:
                    new_dist += 0.5

                if new_dist < 1: 
                    dist_dict[frozenset([a, m])] = new_dist

    # g and k syllables (except in "ka" and "ga" because they have different characters)
    # have 0.25 distance, like dl- and tl-
    dist_dict.update(add_semi_dists(g_sounds, k_sounds))
    dist_dict[frozenset(["ga", "ka"])] = 0.5

    # (vowel) and (' vowel) matches have a distance of 0.25 instead of 0 or 1
    for v in vowels:
        dist_dict[frozenset([v, "'" + v])] = 0.25

    # TODO: save this to a json file and add option for loading it
    # so we don't have to generate all this every time.
    # Then, we can perform properties-based testing:
    # we can calculate the approximate size of how big we expect the dictionary to be.

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