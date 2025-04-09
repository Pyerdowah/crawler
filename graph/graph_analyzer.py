import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import linregress
import random

def analyze_graph(G):
    print("📊 Podstawowe informacje:")
    print(f" - Wierzchołki: {G.number_of_nodes()}")
    print(f" - Krawędzie: {G.number_of_edges()}")

    print("\n🔄 Składowe spójności:")
    print(f" - Liczba słabych składowych spójności (WCC): {nx.number_weakly_connected_components(G)}")
    print(f" - Liczba silnych składowych spójności (SCC): {nx.number_strongly_connected_components(G)}")

    largest_scc = max(nx.strongly_connected_components(G), key=len)
    print(f" - Rozmiar największej SCC: {len(largest_scc)}")

    print("\n📈 Rozkłady stopni:")
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    _plot_degree_distribution(list(in_degrees.values()), "In-degree")
    _plot_degree_distribution(list(out_degrees.values()), "Out-degree")

    print("\n📐 Najkrótsze ścieżki (w największej SCC):")
    H = G.subgraph(largest_scc).copy()
    lengths = dict(nx.all_pairs_shortest_path_length(H))
    path_lengths = [l for d in lengths.values() for l in d.values()]
    avg_distance = np.mean(path_lengths)
    diameter = max(path_lengths)
    print(f" - Średnia długość ścieżki: {avg_distance:.2f}")
    print(f" - Średnica: {diameter}")
    _plot_histogram(path_lengths, "Długości ścieżek (SCC)")

    print("\n🔗 Klasteryzacja:")
    clustering = nx.clustering(H.to_undirected())
    avg_clustering = np.mean(list(clustering.values()))
    print(f" - Średni współczynnik klasteryzacji: {avg_clustering:.4f}")
    _plot_histogram(list(clustering.values()), "Klasteryzacja lokalna")

    print("\n🛡️ Odporność na awarie i ataki:")
    _simulate_failures_and_attacks(G)

    print("\n🔍 Spójność wierzchołkowa:")
    if nx.is_connected(G.to_undirected()):
        print(" - Graf jest spójny (1-spójny)")
        ap = list(nx.articulation_points(G.to_undirected()))
        print(f" - Punkty artykulacji: {len(ap)}")
    else:
        print(" - Graf NIE jest spójny. Szukam par rozspajających...")
        try:
            nc = nx.node_connectivity(G.to_undirected())
            print(f" - Spójność wierzchołkowa: {nc}")
        except Exception as e:
            print(f" - Nie udało się policzyć: {e}")


def _plot_degree_distribution(degrees, label):
    counts = Counter(degrees)
    x_vals, y_vals = zip(*sorted(counts.items()))
    x = []
    y = []
    for xi, yi in zip(x_vals, y_vals):
        if xi > 0 and yi > 0:
            x.append(xi)
            y.append(yi)

    plt.figure()
    plt.loglog(x, y, marker='o', linestyle='None')
    plt.title(f"Rozkład stopni: {label}")
    plt.xlabel("Stopień")
    plt.ylabel("Liczba wierzchołków")
    plt.grid(True)
    plt.show()

    if len(x) >= 2:
        log_x = np.log10(x)
        log_y = np.log10(y)
        slope, intercept, r_value, _, _ = linregress(log_x, log_y)
        print(f" - {label} ~ x^{slope:.2f}, R²={r_value ** 2:.2f}")
    else:
        print(f" - {label}: zbyt mało danych do regresji.")


def _plot_histogram(data, title):
    plt.figure()
    plt.hist(data, bins=30)
    plt.title(title)
    plt.xlabel("Wartość")
    plt.ylabel("Liczba wystąpień")
    plt.grid(True)
    plt.show()

def _simulate_failures_and_attacks(G, remove_frac=0.1):
    N = G.number_of_nodes()
    n_remove = int(N * remove_frac)

    print(f" - Symuluję awarię (losowe usunięcie {n_remove} wierzchołków)...")
    random_nodes = random.sample(list(G.nodes()), n_remove)
    G_fail = G.copy()
    G_fail.remove_nodes_from(random_nodes)
    print(f"   Po awarii - WCC: {nx.number_weakly_connected_components(G_fail)}, SCC: {nx.number_strongly_connected_components(G_fail)}")

    print(f" - Symuluję atak (usunięcie top {n_remove} wierzchołków o najwyższym stopniu)...")
    high_degree_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:n_remove]
    G_attack = G.copy()
    G_attack.remove_nodes_from([n for n, _ in high_degree_nodes])
    print(f"   Po ataku - WCC: {nx.number_weakly_connected_components(G_attack)}, SCC: {nx.number_strongly_connected_components(G_attack)}")

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


