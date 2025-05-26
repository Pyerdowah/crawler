import os
import re
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def load_html_documents(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                # Extract main text (skip scripts/styles)
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

def vectorize_tfidf(docs):
    tfidf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=5)
    X_tfidf = tfidf_vectorizer.fit_transform(docs)
    return X_tfidf, tfidf_vectorizer

def apply_lsi(X_tfidf, n_components=100):
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    X_lsi = svd.fit_transform(X_tfidf)
    return X_lsi, svd


def cluster_docs(X_lsi, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X_lsi)
    return labels, kmeans

def evaluate_clustering(X, labels):
    sil = silhouette_score(X, labels)
    ch = calinski_harabasz_score(X, labels)
    db = davies_bouldin_score(X, labels)
    print(f"Silhouette Score: {sil:.3f}")
    print(f"Calinski-Harabasz Index: {ch:.2f}")
    print(f"Davies-Bouldin Index: {db:.2f}")


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
    print("Top 5 PageRank nodes:", sorted(pr.items(), key=lambda x: x[1], reverse=True)[:5])
    print("Top 5 Degree Centrality nodes:", sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:5])
    return pr, deg_cent


def visualize_clusters(X_lsi, labels):
    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X_lsi)
    plt.figure(figsize=(10, 6))
    plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='tab10')
    plt.title("LSI + KMeans Clustering Visualization")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.colorbar(label="Cluster")
    plt.grid(True)
    plt.show()

def pagerank_vs_clusters(pr_scores, kmeans_labels):
    print("\n📊 PageRank vs KMeans Clusters:")
    top_nodes = sorted(pr_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    for i, (node_id, score) in enumerate(top_nodes):
        cluster_id = kmeans_labels[node_id]
        print(f"Top {i+1}: Doc {node_id}, PageRank={score:.6f}, Cluster={cluster_id}")

def visualize_graph_clusters(G, labels, title="Graph colored by KMeans clusters"):
    import matplotlib.cm as cm
    pos = nx.spring_layout(G, seed=42, k=0.15)  # układ grafu

    unique_clusters = list(set(labels))
    colors = cm.get_cmap('tab10', len(unique_clusters))

    plt.figure(figsize=(10, 8))
    for cluster_id in unique_clusters:
        nodes = [i for i in G.nodes if labels[i] == cluster_id]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=[colors(cluster_id)],
                               label=f"Cluster {cluster_id}", node_size=50, alpha=0.8)

    nx.draw_networkx_edges(G, pos, alpha=0.1)
    plt.title(title)
    plt.axis('off')
    plt.legend()
    plt.show()

def main():
    folder_path = "../data/html"  # folder z plikami .html
    raw_docs = load_html_documents(folder_path)
    print(f"Loaded {len(raw_docs)} HTML documents.")

    cleaned_docs = [preprocess(doc) for doc in raw_docs]

    X_tfidf, vectorizer = vectorize_tfidf(cleaned_docs)
    X_lsi, svd = apply_lsi(X_tfidf, n_components=100)

    labels, kmeans = cluster_docs(X_lsi, n_clusters=5)
    evaluate_clustering(X_lsi, labels)

    G = build_similarity_graph(X_tfidf)
    pr, deg_cent = analyze_graph(G)

    visualize_clusters(X_lsi, labels)

    pagerank_vs_clusters(pr, labels)
    visualize_graph_clusters(G, labels, title="Graph colored by KMeans clusters")

if __name__ == "__main__":
    main()
