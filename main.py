# here is where external library imports will go
import sys
from pathlib import Path

# a higher-order function which takes all the other functions as arguments
# this will look different as I develop
# note: will probably need some kind of word object
def run(load,
        normalize,
        parse,
        n_gram,
        cosine_similarity,
        output):

    # run all central functions
    A_words, B_words = load()
    A_words, B_words = normalize(A_words, B_words)
    A_words, B_words = parse(A_words, B_words)
    A_words, B_words = n_gram(A_words, B_words)
    G = cosine_similarity(A_words, B_words)
    output(G, 0.0)
    return


# runs generic/generic word-matcher
def main():

    # there may be a better way to do this, but this is what I'm doing for now
    # future idea: tell difference between relative and absolute path?
    if len(sys.argv) == 1:
        # if no additional args, imports for generic word-matcher
        target = str((Path.cwd() / "generic").resolve())
    else:
        # import from folder name specified by CLA
        target = sys.argv[1] # absolute directory

    if target not in sys.path:
        sys.path.insert(0, target)

    # try to import functions from given directory
    # if it fails, throw error with message
    try:
        from loader import load # type: ignore
        from normalizer import normalize # type: ignore
        from parser import parse # type: ignore
        from n_gram import n_gram # type: ignore
        from cosine import cosine_similarity # type: ignore
        from output import output # type: ignore
    except Exception as e:
        print(f"Error Type: {type(e).__name__}")
        class BadImportError(Exception):
            """raised when the given directory doesn't have the right file and function names"""
            pass
        raise BadImportError(f"Bad custom imports from {target}. Do you have all the right script and file names?")
    
    run(load, normalize, parse, n_gram, cosine_similarity, output)

    return 0 # placeholder
    

if __name__ == "__main__":
    main()