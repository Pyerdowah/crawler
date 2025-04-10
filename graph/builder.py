from crawler import WebCrawler
import random

def build_graph(base_url, max_pages=3000, num_threads=10):
    crawler = WebCrawler(base_url, max_pages=max_pages, num_threads=num_threads)
    graph = crawler.crawl()
    return graph

def simulate_failure(G, remove_frac=0.1):
    """Symulacja awarii: usuwa losowo remove_frac wierzchołków z grafu G."""
    G_copy = G.copy()
    n_remove = int(remove_frac * G.number_of_nodes())
    nodes_to_remove = random.sample(list(G_copy.nodes()), n_remove)
    G_copy.remove_nodes_from(nodes_to_remove)
    return G_copy

def simulate_attack(G, remove_frac=0.1):
    """Symulacja ataku: usuwa remove_frac wierzchołków o najwyższym stopniu z grafu G."""
    G_copy = G.copy()
    n_remove = int(remove_frac * G.number_of_nodes())
    nodes_by_degree = sorted(G_copy.degree(), key=lambda x: x[1], reverse=True)
    top_nodes = [n for n, _ in nodes_by_degree[:n_remove]]
    G_copy.remove_nodes_from(top_nodes)
    return G_copy

