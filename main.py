import time

from graph.builder import build_graph
import pickle
from graph.visualisation import visualize_graph

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

url = "https://www.um.edu.mt/"
G = build_graph(url, max_pages=3000, num_threads=16)
time.sleep(10)
print(f"Pobrano graf: {G.number_of_nodes()} wierzchołków, {G.number_of_edges()} krawędzi.")
with open("data/graph.gpickle", "wb") as f:
    pickle.dump(G, f)
visualize_graph(G)