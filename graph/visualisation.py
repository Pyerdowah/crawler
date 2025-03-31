# visualization.py
import networkx as nx
import matplotlib.pyplot as plt
import random


def visualize_graph(G, limit=500, seed=42):
    subgraph_nodes = random.sample(list(G.nodes()), min(limit, len(G)))
    H = G.subgraph(subgraph_nodes)

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(H, seed=seed)

    nx.draw_networkx_nodes(H, pos, node_size=50, node_color='skyblue')
    nx.draw_networkx_edges(H, pos, alpha=0.3)

    plt.title("Podglądowy wycinek grafu połączeń", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
