
# exclusive threshold, which means matches with
# scores strictly GREATER THAN the set threshold
def output(G, threshold_exclusive=float(input("Score threshold (exclusive): ")), outmethod=input("Output format method (leave blank for print to stdout): ")):

    import math

    # print to stdout
    if outmethod == "" or outmethod == "print":

        for l, r, data in G.edges(data=True):
            weight = data['weight']
            if weight <= threshold_exclusive or (math.isclose(weight, 1.0) and l.alt == r.alt):
                continue
            print(f"{l.raw}\t{l.normal}\t{r.raw}\t{r.normal}\t{weight:.4f}")

        #print(threshold_exclusive) # test code

    # save to file (good for big data sets)
    # TODO: add failsafes so I don't explode my hard drive?
    elif outmethod == "save" or outmethod == "file":

        fname = "results"
        f = open(fname, "w+")
        for l, r, data in G.edges(data=True):
                    weight = data['weight']
                    if weight <= threshold_exclusive or (math.isclose(weight, 1.0)  and l.alt == r.alt):
                        continue
                    f.write(f"{l.raw}\t{l.normal}\t{r.raw}\t{r.normal}\t{weight:.4f}\n")

    else:
        print("Invalid output format, returning...")

    # nothing to return
