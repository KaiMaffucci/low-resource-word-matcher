
def normalize(A_words, B_words):

    import unicodedata

    # NFC is good enough for our purposes
    # this is a generic implementation, it's not meant to do anything fancy
    # doing it on the alt text this time; that's where the phonetic (latin) spellings are stored
    for i in range(len(A_words)):
        clean_alt = A_words[i].alt.replace("’", "'").replace("‘", "'").replace("`", "'")
        A_words[i].normal =  unicodedata.normalize('NFC',clean_alt).strip().lower()

    for i in range(len(B_words)):
        clean_alt = B_words[i].alt.replace("’", "'").replace("‘", "'").replace("`", "'")
        B_words[i].normal =  unicodedata.normalize('NFC',clean_alt).strip() # already lowercase here

    return A_words, B_words