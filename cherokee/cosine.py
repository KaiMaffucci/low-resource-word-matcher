
def cosine_similarity(A_words, B_words, S_matrix):

    import networkx as nx
    import numpy as np

    # undirected graph
    G = nx.Graph()

    # add words to both sides of bipartite graph
    G.add_nodes_from(A_words, bipartite=0)
    G.add_nodes_from(B_words, bipartite=1)

    # so I wanted to use Gensim's soft cosine function,
    # but I'd have to transfer my np vecs to Gensim's format,
    # and the computational time that takes makes it not worth it.
    # so I implemented my own
    def soft_cosine(l, r):
        # @ is matrix multiplication
        # .T is transposed vector
        numerator = l @ S_matrix @ r.T
        denom_l = l @ S_matrix @ l.T
        denom_r = r @ S_matrix @ r.T
        # this shouldn't happen, but just in case, avoid division by 0 errors
        # if either is 0, it means the ngram vector was empty (blank word and/or something is wrong)
        if denom_l == 0 or denom_r == 0:
            return 0.0
        return numerator / np.sqrt(denom_l * denom_r)

    # perform soft cosine on each word combo
    for l in A_words:
            lv = l.vec
            for r in B_words:
                rv = r.vec
                score = soft_cosine(lv, rv)
                G.add_edge(l, r, weight = score)

    # return final pairings output
    return G
