import os
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import matplotlib.cm as cm

# ------------------------ Loading and Preprocessing ------------------------

def load_html_documents(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                for tag in soup(["script", "style"]):
                    tag.decompose()
                text = soup.get_text(separator=' ', strip=True)
                docs.append(text)
    return docs

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

# ------------------------ Vectorization and LSI ------------------------

def vectorize_tfidf(docs):
    tfidf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=5)
    X_tfidf = tfidf_vectorizer.fit_transform(docs)
    return X_tfidf, tfidf_vectorizer

def apply_lsi(X_tfidf, n_components=100):
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    X_lsi = svd.fit_transform(X_tfidf)
    return X_lsi, svd

# ------------------------ Clustering ------------------------

def cluster_docs(X_lsi, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X_lsi)
    return labels, kmeans

def evaluate_clustering(X, labels):
    sil = silhouette_score(X, labels)
    ch = calinski_harabasz_score(X, labels)
    db = davies_bouldin_score(X, labels)
    return sil, ch, db

def test_multiple_k_values(X_lsi, k_range=range(2, 11)):
    sil_scores, ch_scores, db_scores = [], [], []
    for k in k_range:
        labels, _ = cluster_docs(X_lsi, n_clusters=k)
        sil, ch, db = evaluate_clustering(X_lsi, labels)
        sil_scores.append(sil)
        ch_scores.append(ch)
        db_scores.append(db)
        print(f"k={k}: Sil={sil:.3f}, CH={ch:.1f}, DB={db:.2f}")

    plt.figure(figsize=(12, 6))
    plt.plot(k_range, sil_scores, marker='o', label='Silhouette Score')
    plt.plot(k_range, ch_scores, marker='x', label='Calinski-Harabasz')
    plt.plot(k_range, db_scores, marker='s', label='Davies-Bouldin (lower better)')
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Score (log scale)")
    plt.yscale('log')
    plt.title("KMeans Evaluation Metrics vs. k (Log Scale)")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

    best_k = k_range[np.argmax(sil_scores)]
    print(f"\n✅ Best k based on Silhouette Score: {best_k}")
    return best_k

# ------------------------ Graph and Centrality ------------------------

def build_similarity_graph(X_tfidf, threshold=0.2):
    similarity = cosine_similarity(X_tfidf)
    G = nx.Graph()
    for i in range(similarity.shape[0]):
        for j in range(i+1, similarity.shape[1]):
            if similarity[i, j] > threshold:
                G.add_edge(i, j, weight=similarity[i, j])
    return G

def analyze_graph(G):
    pr = nx.pagerank(G)
    deg_cent = nx.degree_centrality(G)
    print("\n🏅 Top 5 PageRank:", sorted(pr.items(), key=lambda x: x[1], reverse=True)[:5])
    return pr, deg_cent

# ------------------------ Visualizations ------------------------

def visualize_clusters(X_lsi, labels):
    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X_lsi)
    plt.figure(figsize=(10, 6))
    plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='tab10')
    plt.title("LSI + KMeans Clustering")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.colorbar(label="Cluster")
    plt.grid(True)
    plt.show()

def visualize_graph_clusters(G, labels):
    pos = nx.spring_layout(G, seed=42)
    unique_clusters = list(set(labels))
    cmap = cm.get_cmap('tab10', len(unique_clusters))
    plt.figure(figsize=(10, 8))
    for cid in unique_clusters:
        nodes = [n for n in G.nodes if labels[n] == cid]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=[cmap(cid)],
                               label=f"Cluster {cid}", node_size=50, alpha=0.8)
    nx.draw_networkx_edges(G, pos, alpha=0.1)
    plt.title("Similarity Graph Colored by Cluster")
    plt.legend()
    plt.axis('off')
    plt.show()

# ------------------------ Cluster + Graph Analysis ------------------------

def pagerank_vs_clusters(pr, labels):
    print("\n📌 PageRank vs Clusters:")
    for i, (node, score) in enumerate(sorted(pr.items(), key=lambda x: x[1], reverse=True)[:5]):
        print(f"  Doc {node}: PageRank={score:.4f}, Cluster={labels[node]}")

def analyze_pagerank_by_cluster(pr_scores, labels):
    cluster_pr = defaultdict(list)
    for node, score in pr_scores.items():
        cluster = labels[node]
        cluster_pr[cluster].append((node, score))

    print("\n📊 PageRank – średnie i top 3 w każdym klastrze:")
    for cluster, scores in sorted(cluster_pr.items()):
        scores_sorted = sorted(scores, key=lambda x: x[1], reverse=True)
        avg = np.mean([s for _, s in scores])
        max_score = scores_sorted[0][1]
        print(f"\n🔹 Cluster {cluster}:")
        print(f"   Średni PageRank: {avg:.6f}, Maksymalny: {max_score:.6f}, Liczba dokumentów: {len(scores)}")
        print("   Top 3 dokumenty:")
        for i, (doc_id, score) in enumerate(scores_sorted[:3]):
            print(f"     {i+1}. Doc {doc_id} – PageRank: {score:.6f}")

def print_graph_statistics(G):
    print("\n📈 Statystyki grafu podobieństw:")
    print(f"  Wierzchołki: {G.number_of_nodes()}")
    print(f"  Krawędzie: {G.number_of_edges()}")
    degrees = [d for _, d in G.degree()]
    print(f"  Średni stopień: {np.mean(degrees):.2f}")
    print(f"  Maksymalny stopień: {np.max(degrees)}")
    components = list(nx.connected_components(G))
    print(f"  Składowe spójne: {len(components)}")
    print(f"  Największa składowa: {len(max(components, key=len))}")

# ------------------------ Main ------------------------

def main():
    folder_path = "../data/html"  # zmień na ścieżkę do plików .html
    raw_docs = load_html_documents(folder_path)
    print(f"📄 Załadowano {len(raw_docs)} dokumentów.")
    cleaned = [preprocess(doc) for doc in raw_docs]

    X_tfidf, vectorizer = vectorize_tfidf(cleaned)
    X_lsi, svd = apply_lsi(X_tfidf)

    best_k = test_multiple_k_values(X_lsi, k_range=range(2, 11))
    labels, kmeans = cluster_docs(X_lsi, n_clusters=best_k)

    G = build_similarity_graph(X_tfidf)
    pr, deg_cent = analyze_graph(G)

    sil, ch, db = evaluate_clustering(X_lsi, labels)
    print(f"\n📊 Final Clustering (k={best_k}): Sil={sil:.3f}, CH={ch:.1f}, DB={db:.2f}")

    visualize_clusters(X_lsi, labels)
    visualize_graph_clusters(G, labels)

    pagerank_vs_clusters(pr, labels)
    analyze_pagerank_by_cluster(pr, labels)
    print_graph_statistics(G)

if __name__ == "__main__":
    main()
