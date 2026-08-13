
def cosine_similarity(A_words, B_words):

    import networkx as nx
    import numpy as np

    # undirected graph
    G = nx.Graph()

    # add words to both sides of bipartite graph
    G.add_nodes_from(A_words, bipartite=0)
    G.add_nodes_from(B_words, bipartite=1)

    # calculate basic cosine similarity between all word vectors
    for l in A_words:
        lv = l.vec
        for r in B_words:
            rv = r.vec
            score = np.dot(lv, rv) / (np.linalg.norm(lv) * np.linalg.norm(rv)) 
            G.add_edge(l, r, weight = score)

    return G