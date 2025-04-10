def custom_pagerank(G, d=0.85, max_iter=100, tol=1e-6, verbose=False):
    N = G.number_of_nodes()
    pr = {node: 1.0 / N for node in G}
    sink_nodes = [n for n in G if G.out_degree(n) == 0]

    for it in range(max_iter):
        prev_pr = pr.copy()
        sink_sum = sum(prev_pr[n] for n in sink_nodes)
        for node in G:
            rank = (1 - d) / N
            rank += d * sink_sum / N
            for in_node in G.predecessors(node):
                rank += d * prev_pr[in_node] / G.out_degree(in_node)
            pr[node] = rank

        diff = sum(abs(pr[n] - prev_pr[n]) for n in G)
        if verbose:
            print(f"Iteracja {it + 1}, różnica: {diff:.2e}")
        if diff < tol:
            break
    return pr