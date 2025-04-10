from itertools import combinations

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import linregress
import random

from graph.custom_pagerank import custom_pagerank
from graph.visualisation import visualize_scc_graph


def analyze_connectivity_components(G):
    print("\n🧩 Analiza składowych spójności")

    # WCC
    wcc = list(nx.weakly_connected_components(G))
    print(f" - Liczba słabych składowych spójności (WCC): {len(wcc)}")
    print(f" - Rozmiar największej WCC: {len(max(wcc, key=len))}")

    # SCC
    scc = list(nx.strongly_connected_components(G))
    print(f" - Liczba silnych składowych spójności (SCC): {len(scc)}")
    largest_scc = max(scc, key=len)
    print(f" - Rozmiar największej SCC: {len(largest_scc)}")

    # IN/OUT/SCC/TENDRILS
    G_rev = G.reverse(copy=True)
    scc_set = set(largest_scc)

    reachable_from_scc = set()
    for node in largest_scc:
        reachable_from_scc.update(nx.descendants(G, node))
    reachable_from_scc.update(scc_set)

    reaching_scc = set()
    for node in largest_scc:
        reaching_scc.update(nx.descendants(G_rev, node))
    reaching_scc.update(scc_set)

    IN = reaching_scc - scc_set
    OUT = reachable_from_scc - scc_set
    TENDRILS = set(G.nodes()) - (scc_set | IN | OUT)

    print(f" - IN (prowadzą do SCC): {len(IN)}")
    print(f" - OUT (osiągalne z SCC): {len(OUT)}")
    print(f" - TENDRILS / ISLANDS (poza głównym korpusem): {len(TENDRILS)}")

    # Metagraf (graf SCC)
    G_scc = nx.condensation(G, scc=list(nx.strongly_connected_components(G)))
    print(f" - Wierzchołki w G_SCC (grafie kondensacji): {G_scc.number_of_nodes()}")
    print(f" - Krawędzie w G_SCC: {G_scc.number_of_edges()}")
    visualize_scc_graph(G_scc)

    return {
        'wcc_count': len(wcc),
        'scc_count': len(scc),
        'largest_scc_size': len(largest_scc),
        'IN_size': len(IN),
        'OUT_size': len(OUT),
        'TENDRILS_size': len(TENDRILS),
        'G_SCC': G_scc
    }

def analyze_degree_distribution(G):
    print("\n📊 Rozkłady stopni (log-log + regresja):")

    for kind, deg_func in [("In-degree", G.in_degree), ("Out-degree", G.out_degree)]:
        degrees = [d for _, d in deg_func()]
        counts = Counter(degrees)

        # Usuń zera (log(0) = -inf)
        x_vals, y_vals = zip(*[(k, v) for k, v in counts.items() if k > 0 and v > 0])
        log_x = np.log10(x_vals)
        log_y = np.log10(y_vals)

        # Regresja log-log
        slope, intercept, r_value, _, _ = linregress(log_x, log_y)
        print(f" - {kind}: y = x^{slope:.2f}, R² = {r_value**2:.3f}")

        # Wykres log-log
        plt.figure(figsize=(6, 4))
        plt.loglog(x_vals, y_vals, marker='o', linestyle='None', label='Dane')
        plt.plot(x_vals, 10**(intercept + slope * log_x), label=f'Regresja: x^{slope:.2f}')
        plt.title(f"Rozkład {kind}")
        plt.xlabel("Stopień")
        plt.ylabel("Liczba wierzchołków")
        plt.grid(True, which="both", ls="--")
        plt.legend()
        plt.tight_layout()
        plt.show()

def analyze_shortest_paths(G):
    print("\n🧭 Analiza najkrótszych ścieżek (dla największej SCC):")

    # Znajdź największą SCC
    scc = max(nx.strongly_connected_components(G), key=len)
    H = G.subgraph(scc).copy()

    # Odległości między wszystkimi parami
    all_lengths = dict(nx.all_pairs_shortest_path_length(H))

    node_avg_dists = []
    node_radii = []

    all_distances = []

    for node, targets in all_lengths.items():
        dists = list(targets.values())
        all_distances.extend(dists)
        node_avg_dists.append(np.mean(dists))
        node_radii.append(max(dists))

    avg_path_len = np.mean(all_distances)
    diameter = max(all_distances)

    print(f" - Średnia odległość (dla SCC): {avg_path_len:.2f}")
    print(f" - Średnica (diameter): {diameter}")

    # Histogram średnich odległości z każdego wierzchołka
    plt.figure()
    plt.hist(node_avg_dists, bins=30)
    plt.title("Histogram średnich odległości z wierzchołków")
    plt.xlabel("Średnia odległość")
    plt.ylabel("Liczba wierzchołków")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Histogram promieni
    plt.figure()
    plt.hist(node_radii, bins=30)
    plt.title("Histogram promieni (maksymalnych odległości)")
    plt.xlabel("Promień")
    plt.ylabel("Liczba wierzchołków")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Regresja log-log histogramu średnich odległości
    counts = np.bincount(np.array(node_avg_dists, dtype=int))
    x_vals = np.arange(len(counts))
    y_vals = counts

    mask = (x_vals > 0) & (y_vals > 0)
    log_x = np.log10(x_vals[mask])
    log_y = np.log10(y_vals[mask])

    if len(log_x) > 1:
        slope, intercept, r_value, _, _ = linregress(log_x, log_y)
        print(f" - Regresja histogramu (średnie odległości): x^{slope:.2f}, R²={r_value ** 2:.2f}")
    else:
        print(" - Za mało danych do regresji histogramu.")

    return {
        'avg_path_len': avg_path_len,
        'diameter': diameter,
        'avg_dists': node_avg_dists,
        'radii': node_radii
    }

def analyze_clustering(G):
    print("\n🔗 Współczynniki klasteryzacji:")

    UG = G.to_undirected()
    clustering = nx.clustering(UG)
    values = list(clustering.values())

    global_clustering = nx.average_clustering(UG)
    print(f" - Globalna klasteryzacja: {global_clustering:.4f}")
    print(f" - Liczba wierzchołków z C > 0: {sum(c > 0 for c in values)}")

    # Histogram lokalnych wartości
    plt.figure()
    plt.hist(values, bins=30)
    plt.title("Histogram lokalnych współczynników klasteryzacji")
    plt.xlabel("Współczynnik klasteryzacji")
    plt.ylabel("Liczba wierzchołków")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Przygotowanie do regresji — histogram (binning) wartości > 0
    nonzero = [v for v in values if v > 0]
    bins = np.linspace(0.01, 1.0, 30)
    hist, edges = np.histogram(nonzero, bins=bins)

    x_vals = 0.5 * (edges[:-1] + edges[1:])
    y_vals = hist

    mask = (y_vals > 0)
    log_x = np.log10(x_vals[mask])
    log_y = np.log10(y_vals[mask])

    if len(log_x) > 1:
        slope, intercept, r_value, _, _ = linregress(log_x, log_y)
        print(f" - Regresja histogramu klasteryzacji: x^{slope:.2f}, R²={r_value**2:.2f}")

        # Wykres log-log histogramu z regresją
        plt.figure()
        plt.loglog(x_vals[mask], y_vals[mask], 'o', label='Dane')
        plt.loglog(x_vals[mask], 10**(intercept + slope * log_x), label=f'Regresja: x^{slope:.2f}')
        plt.title("Rozkład lokalnej klasteryzacji (log-log)")
        plt.xlabel("Współczynnik klasteryzacji")
        plt.ylabel("Liczba wierzchołków")
        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.tight_layout()
        plt.show()
    else:
        print(" - Za mało danych do regresji klasteryzacji.")

def analyze_vertex_connectivity(G):
    print("\n🧩 Spójność wierzchołkowa:")

    UG = G.to_undirected()
    if not nx.is_connected(UG):
        print(" - Graf niespójny → brak sensu szukać rozspajających wierzchołków.")
        return

    connectivity = nx.node_connectivity(UG)
    print(f" - Spójność wierzchołkowa: {connectivity}")

    if connectivity == 1:
        print(" - Szukanie wierzchołków rozspajających (punkty artykulacji)...")
        articulation = list(nx.articulation_points(UG))
        print(f"   Znaleziono {len(articulation)} punktów artykulacji.")
        print("   Przykład:", articulation[:5])
    elif connectivity == 2:
        print(" - Szukanie par wierzchołków rozspajających (może być kosztowne)...")
        cut_pairs = []
        nodes = list(UG.nodes())
        for u, v in combinations(nodes, 2):
            UG_copy = UG.copy()
            UG_copy.remove_nodes_from([u, v])
            if not nx.is_connected(UG_copy):
                cut_pairs.append((u, v))
                if len(cut_pairs) >= 5:
                    break
        print(f"   Przykładowe pary rozspajające: {cut_pairs}")
    else:
        print(" - Graf ma spójność ≥ 3 → brak rozspajających pojedynczych/podwójnych.")

def analyze_pagerank_distribution(pr_dict, title="Rozkład PageRank"):
    import matplotlib.pyplot as plt
    from collections import Counter
    from scipy.stats import linregress
    import numpy as np

    values = sorted(pr_dict.values(), reverse=True)
    ranks = list(range(1, len(values) + 1))

    plt.figure()
    plt.loglog(ranks, values, marker='o', linestyle='None')
    plt.title(title)
    plt.xlabel("Ranga")
    plt.ylabel("PageRank")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Regresja log-log
    log_x = np.log10(ranks)
    log_y = np.log10(values)
    slope, intercept, r_value, _, _ = linregress(log_x, log_y)
    print(f" - Regresja log-log: y ~ x^{slope:.2f}, R² = {r_value**2:.3f}")

def pagerank_convergence_study(G, d_values=[0.6, 0.75, 0.85, 0.95, 1.0]):
    print("\n🔁 Zbieżność PageRank dla różnych współczynników tłumienia:")
    for d in d_values:
        print(f"\nDamping = {d}")
        pr = custom_pagerank(G, d=d, verbose=True)
        top = sorted(pr.items(), key=lambda x: x[1], reverse=True)[:5]
        print("Top 5 stron:")
        for node, val in top:
            print(f"  {node[:60]}... : {val:.4e}")
        analyze_pagerank_distribution(pr, title=f"PageRank (d={d})")




