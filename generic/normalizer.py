
def normalize(A_words, B_words):

    import unicodedata

    # NFC is good enough for our purposes
    # this is a generic implementation, it's not meant to do anything fancy
    for i in range(len(A_words)):
        A_words[i].normal =  unicodedata.normalize('NFC', A_words[i].raw).strip()

    for i in range(len(B_words)):
        B_words[i].normal =  unicodedata.normalize('NFC', B_words[i].raw).strip()

    return A_words, B_words