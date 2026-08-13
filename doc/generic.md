
# Overview

This is the generic version of the project. This may have more functionality in the future, but it mainly consists of a baseline template. It also demonstrates that I am at least capable of basic NLP work.

I may add type infrencing in some of my function definitions at some point.

IMPORTANT NOTE: This requires `networkx` and `numpy` as installed dependencies, which you can install using pip.

## loader.py

`load(A, B) -> A_words, B_words`: takes two file names as input, but by default, it will ask the user to input the names as text. Note that execution occurs from the root of the project, so to use `foo.txt` in the tests folder, you would need to specify `tests/foo.txt`.

## parser.py

`parse(A_words, B_words) -> A_words, B_words` takes two sets of words (expected to be WordObj instances) and fills in the `morphemes` member data in each. The generic version is extremely simple, so it just counts each character as a morpheme.

## normalizer.py

`normalize(A_words, B_words) -> A_words, B_words` takes two sets of WordObj instances and adds the data member for `normal` in each, normalizing each word. Doesn't really do too much. I debated putting it before parsing, but ultimately left it the way it is.

## n_gram.py

`n_gram(A_words, B_words) -> A_words, B_words`: contains the entire workflow. It takes the two WordObj lists as input, generates the n-grams for each word, builds a vocabulary from the n-grams, then generates vectors off of the n-grams and the total vocabulary. It functions a bit fundamentally different from how the Cherokee version likely will. The Cherokee version will have a pre-defined, manually-generated vocabulary of n-grams, rather than just generating one based on the current n-grams like this one does. Default `n=2`.

`tokenize(words) -> words`: takes a **single** list of WordObj instances and generates the n-grams for each instance in the list.

`build_vocab(ngrams) -> vocab`: builds a vocabulary dictionary, where each n-gram will correspond to an index in the vector.

`vectorize(words) -> words`: takes a list of WordObj instances and a vocuabulary dictionary, expected to have n-grams generated, and generates the corresponding vectors in each instance.

## cosine.py

`cosine_similarity(A_words, B_words) -> G`: Creates a bipartite graph using the two words lists, where the weight of each edge is the cosine similarity score.

## output.py

`output(G, threshold, outmethod) -> None`: Outputs each word pair and their respective scores. For now, it only outputs to stdout using print.
