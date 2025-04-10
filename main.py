import time

from graph.builder import build_graph, simulate_failure, simulate_attack
import pickle
import networkx as nx

from graph.custom_pagerank import custom_pagerank
from graph.graph_analyzer import analyze_connectivity_components, analyze_degree_distribution, analyze_shortest_paths, \
    analyze_clustering, analyze_vertex_connectivity, analyze_pagerank_distribution, pagerank_convergence_study
from graph.visualisation import visualize_graph, visualize_scc_graph


def test_on_threads(base_url, max_pages=200, thread_options=[1, 2, 4, 8, 16]):
    results = []

    for threads in thread_options:
        print(f"\n--- Test: {threads} wątków ---")
        start = time.time()
        G = build_graph(base_url, max_pages=max_pages, num_threads=threads)
        end = time.time()
        duration = end - start
        results.append((threads, duration, G.number_of_nodes(), G.number_of_edges()))

    print("\nWyniki:")
    for threads, dur, nodes, edges in results:
        print(f"{threads} wątków → {dur:.2f}s, {nodes} wierzchołków, {edges} krawędzi")

    return results

# url = "https://www.um.edu.mt/"
# G = build_graph(url, max_pages=3000, num_threads=16)
# time.sleep(10)
# print(f"Pobrano graf: {G.number_of_nodes()} wierzchołków, {G.number_of_edges()} krawędzi.")
with open("data/graph.gpickle", "rb") as f:
    G = pickle.load(f)

# for remove_frac in [0.1, 0.3, 0.5]:
#     F = simulate_failure(G, remove_frac=remove_frac)
#     print(f"Pobrano graf: {F.number_of_nodes()} wierzchołków, {F.number_of_edges()} krawędzi.")
#     analyze_connectivity_components(F)
#     analyze_degree_distribution(F)
#     analyze_shortest_paths(F)
#     analyze_clustering(F)
#     analyze_vertex_connectivity(F)
#     A = simulate_attack(G, remove_frac=remove_frac)
#     print(f"Pobrano graf: {A.number_of_nodes()} wierzchołków, {A.number_of_edges()} krawędzi.")
#     analyze_connectivity_components(A)
#     analyze_degree_distribution(A)
#     analyze_shortest_paths(A)
#     analyze_clustering(A)
#     analyze_vertex_connectivity(A)

# 1. PageRank bez tłumienia
pr1 = custom_pagerank(G, d=1.0)
analyze_pagerank_distribution(pr1, "PageRank bez tłumienia")

# 2. PageRank z tłumieniem
pr2 = custom_pagerank(G, d=0.85)
analyze_pagerank_distribution(pr2, "PageRank z tłumieniem d=0.85")

# 3. Zbieżność dla wielu wartości
pagerank_convergence_study(G, d_values=[0.6, 0.75, 0.85, 0.95, 1.0])