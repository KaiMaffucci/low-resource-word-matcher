
def normalize(A_words, B_words):

    import unicodedata

    # NFC is good enough for our purposes
    # this is a generic implementation, it's not meant to do anything fancy
    # doing it on the alt text this time; that's where the phonetic (latin) spellings are stored
    for i in range(len(A_words)):
        A_words[i].normal =  unicodedata.normalize('NFC', A_words[i].alt).strip().lower()

    for i in range(len(B_words)):
        B_words[i].normal =  unicodedata.normalize('NFC', B_words[i].alt).strip() # already lowercase here

    return A_words, B_words