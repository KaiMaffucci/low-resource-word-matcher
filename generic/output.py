
"""
Outputs data. 

G: a bipartite graph
threshold: the minimum similarity two words have to have to be outputted
outmethod: how the user wants the data to be outputted/stored.\
                        Just prints for now, but later functionality for csv, tsv, etc may become available (especially in Cherokee version)
"""
def output(G, threshold=0.7, outmethod=input("Output format method (leave blank for print to stdout): ")):

    if outmethod == "" or outmethod == "print":

        for l, r, data in G.edges(data=True):
            weight = data['weight']

            if weight < threshold:
                continue
            
            # Use .name if your node is an object, or just print the node directly if it's a string
            print(f"{l.normal} \t|\t {r.normal} | Weight: {weight:.4f}")

    else:
        print("Invalid output format, returning...")