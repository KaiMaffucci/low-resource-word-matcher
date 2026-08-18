
def parse(A_words, B_words):

    # generic parser: each character is a morpheme (this is pretty terrible)
    
    for i in range(len(A_words)):
        A_words[i].morphemes = list(A_words[i].normal)

    for i in range(len(B_words)):
        B_words[i].morphemes = list(B_words[i].normal)

    return A_words, B_words