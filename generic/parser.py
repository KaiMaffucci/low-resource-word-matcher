
def parse(A_words, B_words):

    # generic parser: each character is a morpheme (this is pretty terrible)
    
    for i in range(len(A_words)):
        A_words[i].morphemes = list(A_words[i].raw)

    for i in range(len(B_words)):
        B_words[i].morphemes = list(B_words[i].raw)

    # test code
    for word in A_words:
        print(word.morphemes)

    for word in B_words:
        print(word.morphemes)

    return A_words, B_words