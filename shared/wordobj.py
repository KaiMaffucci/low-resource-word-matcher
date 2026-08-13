

"""
Object which stores information about our words
will be updated to contain other important data, but as of now:

raw: raw text extracted from file/original text of word
alt: an alternative spelling of original text (perhaps a different script)

morphemes: parsed list of morphemes
normal: normalized version of word
ngrams: n-gram tokenization
self.vec: vectorization of n-gram tokens
"""

class WordObj:
    
    def __init__(self, raw="", alt=""):
        self.raw = raw
        self.alt = alt
        self.morphemes = []
        self.normal = []
        self.ngrams = []
        self.vec = None
