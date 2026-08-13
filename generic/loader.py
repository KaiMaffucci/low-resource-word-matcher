

"""
loads text from files (A and B) into lists

A: file name of words set A
B: file name of words of set B
d: data delimiter/seperator (tab, comma, etc)  
"""


def load(A=input("File with set A words: "), B = input("File with set B words: ")):

    from shared.wordobj import WordObj

    A_words = []
    with open(A, "r") as A_file:
        for line in A_file:
            A_words.append(WordObj(line.strip()))

    B_words = []
    with open(B, "r") as B_file:
            for line in B_file:
                B_words.append(WordObj(line.strip()))

    return A_words, B_words 

