# visualization.py
import networkx as nx
import matplotlib.pyplot as plt
import random


def visualize_graph(G, limit=500, seed=42):
    subgraph_nodes = random.sample(list(G.nodes()), min(limit, len(G)))
    H = G.subgraph(subgraph_nodes)

    plt.figure(figsize=(12, 12))
    pos = nx.kamada_kawai_layout(H)

    nx.draw_networkx_nodes(H, pos, node_size=50, node_color='skyblue')
    nx.draw_networkx_edges(H, pos, alpha=0.3)

    plt.title("Podglądowy wycinek grafu połączeń", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def visualize_scc_graph(G_scc):
    sizes = [len(G_scc.nodes[n]['members']) * 10 for n in G_scc.nodes]

    plt.figure(figsize=(12, 10))
    pos = nx.kamada_kawai_layout(G_scc)

    nx.draw_networkx_nodes(G_scc, pos,
                           node_size=sizes,
                           node_color='skyblue',
                           alpha=0.8,
                           linewidths=0.5,
                           edgecolors='gray')

    nx.draw_networkx_edges(G_scc, pos,
                           arrows=True,
                           alpha=0.4)

    plt.title("Graf SCC (kondensacja silnie spójnych składowych)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()