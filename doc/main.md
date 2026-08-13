
# How To Run The Project: main.py

Executing `main.py` will run the main script, prompting the user for a folder path to which version you want to run. Leave blank to use the generic version by default. 

The meat of `main.py` is the `run()` function. This takes six functions as input, which `run()` sequentially executes. I designed it this way so that any future versions of the project will use this general format.

## shared/wordobj.py

This file contains the central class definition I use to organize word data throughout the project. It has some useful data members, capable of storing the original text, the parsed list of morphemes, the normalized list of morphemes, the ngrams list of tuples for the word, and the vectorization of the word.
