from graph.builder import build_graph
import pickle
from graph.visualisation import visualize_graph

url = "https://www.upv.es/"
G = build_graph(url, max_pages=30, num_threads=10)
print(f"Pobrano graf: {G.number_of_nodes()} wierzchołków, {G.number_of_edges()} krawędzi.")
with open("data/graph.gpickle", "wb") as f:
    pickle.dump(G, f)
visualize_graph(G)
