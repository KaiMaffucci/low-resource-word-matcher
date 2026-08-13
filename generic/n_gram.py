
#from shared.wordobj import WordObj

def n_gram(A_words, B_words, n=2):

    # generate n-grams for each word in each set
    A_words = tokenize(A_words, n)
    B_words = tokenize(B_words, n)

    # build vocab for vectorization
    all_ngrams = [
        ngram 
        for word in (A_words + B_words) 
        for ngram in word.ngrams
    ]
    vocab = build_vocab(all_ngrams)

    # generate a vector for each word's n-gram list
    A_words = vectorize(A_words, vocab)
    B_words = vectorize(B_words, vocab)

    return A_words, B_words


def tokenize(words, n):

    for w in range(len(words)):
        # crazy freaking trick
        words[w].ngrams = list(zip(*(words[w].morphemes[i:] for i in range(n))))

    return words


def build_vocab(all_ngrams):

    vocab = set()

    # adds every gram to vocab set
    for ngram in all_ngrams:
        vocab.add(ngram)

    # maps each gram to sorted index position
    # another crazy trick
    return {ngram: i for i, ngram in enumerate(sorted(vocab))}


def vectorize(words, vocab):

    # vectorizes individual word
    from collections import Counter

    def vectorize_word(ngrams):

        # n-gram frequency 
        counts = Counter(ngrams)

        # empty vector size of vocab
        new_vec = [0] * len(vocab)

        # set each index of vector to count of corresponding ngram
        for ngram, count in counts.items():
            if ngram in vocab: # always true
                new_vec[vocab[ngram]] = count

        return new_vec

    # for each word, takes ngrams and calculates vector based off it
    for i in range(len(words)):
        words[i].vec = vectorize_word(words[i].ngrams)

    return words

