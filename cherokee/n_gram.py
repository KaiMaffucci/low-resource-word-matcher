
# NOTE: "nah" syllable is kind of a problem?
def n_gram(A_words, B_words, n=1):

    if n != 1:
        print("We don't do real n-grams here, sorry. Running default \"n=1\"...")

    # build custom distances morpheme-to-morpheme (TODO: property-based testing on dictionary size)
    all_morphemes, dist_dict = build_dist_dict()

    # map each morpheme to an index for vectorization
    index_map = {m: i for i, m in enumerate(all_morphemes)}

    """
    TEST: morpheme dictionary size is valid
    standard syllabry => +86
    standard standalone consonant sounds => +15
    spelling variants (including standalone consonants) 
        dl_ (- tla), k_ (- ka), j_/ch_, gw_/gu_/kw_ => +6+6+14+21
                                                                                                        - 1 ("gu" is double-counted for because it is a consonant and "g" + "u")
    current total: 147
    aspirated sounds (note: realistically morphemes like "hh" don't exist, but they are includeed) => +147-2-6 (hna does not get a "hhna" and "hna" already counted; so are "h_" sounds)
    glottal-initial sounds => *2
    total: 572
    """
    real_m_count = 572
    try: 
        assert(len(all_morphemes) == real_m_count)
    except AssertionError:
        print(f"ASSERT FAIL: Expected morpheme count:{real_m_count}, got: {len(all_morphemes)}")
        exit()

    # TEST: morphemes list and index map match
    try:
        assert(len(all_morphemes) == len(index_map))
    except AssertionError:
        print(f"ASSERT FAIL: Morpheme list size does not match index map size")
        exit()

    # potential future test: do math on proper size of dist_dict
    # (which leads to the shape of the similarity matrix, too)
    # and check for that

    # create sparse similarity matrix 
    S = build_unigram_matrix(index_map, dist_dict)

    # use new index mapping to vectorize words
    A_words = vectorize(A_words, index_map)
    B_words = vectorize(B_words, index_map)

    # vectorization complete
    return A_words, B_words, S

def build_unigram_matrix(index_map, dist_dict):
    import numpy as np

    # initialize matrix 
    map_size = len(index_map)
    S = np.identity(map_size, dtype=np.float32)

    # main loop, adding similarity scores for each morpheme pair
    for f_set, dist in dist_dict.items():
        m1, m2 = list(f_set)
        if m1 in index_map and m2 in index_map:
            i, j = index_map[m1], index_map[m2]
            sim = max(0.0, 1.0 - dist) # linear conversion from dist to sim
            S[i, j] = sim
            S[j, i] = sim
            
    return S

# takes a list of words and generates a vector for each word
def vectorize(words, index_map):
    import numpy as np

    # loop to vectorize each word
    for i in range(len(words)):
        words[i].vec = np.zeros(len(index_map), dtype=np.float32)
        for m in words[i].morphemes:
            if m in index_map:
                words[i].vec[index_map[m]] += 1
    
    return words

# generates custom distances dictionary
def build_dist_dict():
    
    # build massive list of all morphemes based on my grammar
    """
    GRAMMAR (with or's after each line):
    'nah | 'nah
    nah | hna
    'h consonant vowel
    h consonant vowel
    'consonant vowel
    consonant vowel
    ' vowel
    vowel
    'h consonant
    h consonant
    ' consonant
    consonant
    """
    # set to force uniqueness
    all_morphemes = set()

    consonants = ["ts", "j", "ch", "qu", "gw", "kw", "gu", "tl", "d", "dl", "g", "k", "h", "l", "m", "n", "s", "t", "w", "y"]
    vowels = ["a", "e", "i", "o", "u", "v"]

    all_morphemes.add("nah")
    #all_morphemes.add("hna")
    #all_morphemes.add("dla")
    h = "h" # makes life slightly easier
    for c in consonants:
        all_morphemes.add(c)
        all_morphemes.add(h + c) # aspirated morphemes
        for v in vowels:
            all_morphemes.add(h + c + v)
            all_morphemes.add(c + v)
    for v in vowels:
        all_morphemes.add(v)
    all_morphemes.add("s")
    all_morphemes.add("hnah") # edge case aspirated morpheme

    # make it a list so it's easier to iterate
    # does not include glottal stops for now
    all_morphemes = list(all_morphemes)

    # generate lists for custom distance rules
    # add all syllables including standalone consonants/vowels
    # TODO: maybe put this in a function? also maybe use regex instead of this way?
    # it looks atrocious right now, so I should definitely clean it up at some point, but it works right now
    ts_sounds = [m for m in all_morphemes if m[:-1] == "ts"] + ["ts"]
    j_sounds = [m for m in all_morphemes if m[:-1] == "j"] + ["j"]
    ch_sounds = [m for m in all_morphemes if m[:-1] == "ch"] + ["ch"]

    qu_sounds = [m for m in all_morphemes if m[:-1] == "qu"] + ["qu"]
    gw_sounds = [m for m in all_morphemes if m[:-1] == "gw"] + ["gw"]
    gu_sounds = [m for m in all_morphemes if m[:-1] == "gu"] + ["gu"]
    kw_sounds = [m for m in all_morphemes if m[:-1] == "kw"] + ["kw"]

    tl_sounds = [m for m in all_morphemes if m[:-1] == "tl"] + ["tl"]
    dl_sounds = [m for m in all_morphemes if m[:-1] == "dl"] + ["dl"]
    d_sounds = [m for m in all_morphemes if m[:-1] == "d"] + ["d"]
    g_sounds = [m for m in all_morphemes if m[:-1] == "g"] + ["g"]
    k_sounds = [m for m in all_morphemes if m[:-1] == "k"] + ["k"]
    h_sounds = [m for m in all_morphemes if m[:-1] == "h"] + ["h"] # NOTE: *not* aspiration (h before consonant). This is for normal h syllables
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
    dist_dict.update(add_dists(ch_sounds))    

    dist_dict.update(add_dists(qu_sounds))
    dist_dict.update(add_dists(kw_sounds))
    dist_dict.update(add_dists(gw_sounds))
    dist_dict.update(add_dists(gu_sounds))

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
    ts_alikes = [ts_sounds, j_sounds, ch_sounds]
    for sounds_list1 in ts_alikes:
        for sounds_list2 in ts_alikes:
            if sounds_list1 != sounds_list2:
                dist_dict.update(add_equ_dists(sounds_list1, sounds_list2))

    qu_alikes = [qu_sounds, kw_sounds, gu_sounds, gw_sounds]
    for sounds_list1 in qu_alikes:
            for sounds_list2 in qu_alikes:
                if sounds_list1 != sounds_list2:
                    dist_dict.update(add_equ_dists(sounds_list1, sounds_list2))

    # dl + tl (except dla and tla) have 0.25 distance for matching vowel morphemes, nonmatching vowels have 0.75 distance
    dist_dict.update(add_semi_dists(dl_sounds, tl_sounds))
    dist_dict[frozenset(["dla", "tla"])] = 0.5

    # to, tu, tv don't have syllabry symbols,
    # so they will be considered 0.25 distance for matching vowels
    # and 0.75 for nonmatching
    # (like the case with most tl_)
    misc_t_sounds = ['to', 'tu', 'tv']
    add_semi_dists(d_sounds, misc_t_sounds)

    # g and k syllables (except in "ka" and "ga" because they have different characters)
    # have 0.25 distance, like dl- and tl-
    dist_dict.update(add_semi_dists(g_sounds, k_sounds))
    dist_dict[frozenset(["ga", "ka"])] = 0.5

    # build list of aspirated morphemes
    aspirated_morphemes = [m for m in all_morphemes if m[0] == 'h' and m not in h_sounds and m != 'hna']
    # (h consonant [vowel]) have distance of 0.25 from original matching (consonant vowel)
    def build_aspirated_distances(aspirated_morphemes, is_glottal=0): # is_glottal = 1 means there is a ' at start of morpheme
        for a in aspirated_morphemes:
            new_dists = {}
            # list comprehension includes
            for m in all_morphemes:
                new_dist = 0
                if a != m:
                    # normal h sounds
                    if m in h_sounds:
                        # if vowels match
                        if a[-1] == m[-1]:
                            new_dists[frozenset([a, m])] = 0.5
                            continue # yeah
                                        
                    # if aspirated consonant in a == consonant in m
                    if a[1+is_glottal:-1] == m[:-1]:
                        new_dist += 0.25
                    else:
                        new_dist += 0.5
                    # if vowels don't match, increase distance
                    if a[-1] != m[-1]:
                        new_dist += 0.5
    
                    if new_dist < 1: 
                        new_dists[frozenset([a, m])] = new_dist
        return new_dists

    dist_dict.update(build_aspirated_distances(aspirated_morphemes))

    # build list of morphemes that start with glottal stop : based on copy of current morpheme list
    glottal_initial_morphemes = ["'" + m for m in all_morphemes]

    # add distances between the glottal initial  morphemes themselves
    dist_dict.update(add_dists(["'" + m for m in ts_sounds]))
    dist_dict.update(add_dists(["'" + m for m in j_sounds]))
    dist_dict.update(add_dists(["'" + m for m in ch_sounds]))

    dist_dict.update(add_dists(["'" + m for m in qu_sounds]))
    dist_dict.update(add_dists(["'" + m for m in kw_sounds]))
    dist_dict.update(add_dists(["'" + m for m in gu_sounds]))
    dist_dict.update(add_dists(["'" + m for m in gw_sounds]))

    dist_dict.update(add_dists(["'" + m for m in tl_sounds]))
    dist_dict.update(add_dists(["'" + m for m in d_sounds]))
    dist_dict.update(add_dists(["'" + m for m in dl_sounds]))
    dist_dict.update(add_dists(["'" + m for m in g_sounds]))
    dist_dict.update(add_dists(["'" + m for m in k_sounds]))
    dist_dict.update(add_dists(["'" + m for m in h_sounds]))
    dist_dict.update(add_dists(["'" + m for m in l_sounds]))
    dist_dict.update(add_dists(["'" + m for m in m_sounds]))
    dist_dict.update(add_dists(["'" + m for m in n_sounds]))
    dist_dict.update(add_dists(["'" + m for m in s_sounds]))
    dist_dict.update(add_dists(["'" + m for m in t_sounds]))
    dist_dict.update(add_dists(["'" + m for m in w_sounds]))
    dist_dict.update(add_dists(["'" + m for m in y_sounds]))

    dist_dict.update(add_dists(["'" + m for m in a_sounds]))
    dist_dict.update(add_dists(["'" + m for m in e_sounds]))
    dist_dict.update(add_dists(["'" + m for m in i_sounds]))
    dist_dict.update(add_dists(["'" + m for m in o_sounds]))
    dist_dict.update(add_dists(["'" + m for m in u_sounds]))
    dist_dict.update(add_dists(["'" + m for m in v_sounds]))

    dist_dict.update(add_equ_dists([ "'" + m for m in ts_sounds], [ "'" + m for m in j_sounds]))

    dist_dict.update(add_semi_dists([ "'" + m for m in dl_sounds], [ "'" + m for m in tl_sounds]))
    dist_dict[frozenset(["'dla", "'tla"])] = 0.5

    # glottal initial morphemes
    glottal_initial_aspirated_morphemes = ["'" + a for a in aspirated_morphemes]
    dist_dict.update(build_aspirated_distances(glottal_initial_aspirated_morphemes))

    # (glottal stop initial morphemes) g and k syllables (except in "ka" and "ga" because they have different characters)
    # have 0.25 distance, like dl- and tl-
    dist_dict.update(add_semi_dists(g_sounds, k_sounds))
    dist_dict[frozenset(["'ga", "'ka"])] = 0.5

    # add distances between the glottal initial morphemes and their original morphemes (new distance *= 1.25)
    for m in all_morphemes:
        dist_dict[frozenset([m, "'" + m])] = 0.1

    # add distances between glottal initial morphemes and non-glottal initial morphemes
    # excluding cases where glottal is only difference
    for m in all_morphemes:
        for g in glottal_initial_morphemes:
            if frozenset([m, g[1:]]) in dist_dict:
                dist_dict[frozenset([m, g])] = dist_dict[frozenset([m, g[1:]])] * 1.1

    # TODO: save this to a json file and add option for loading it
    # so we don't have to generate all this every time.
    # Then, we can perform properties-based testing:
    # we can calculate the approximate size of how big we expect the dictionary to be.

    all_morphemes += glottal_initial_morphemes

    # for testing
    """
    import json
    for_json = {str(tuple(sorted(list(k)))): v for k, v in dist_dict.items()}
    with open("dist_dict.json", "w+") as file:
        json.dump(for_json, file, indent=4)
    """

    return all_morphemes, dist_dict
