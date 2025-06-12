C:\Python311\python.exe C:\Users\Paulina\Desktop\mgr\sem3\crawler\p2\lsi_clustering_analysis.py 
📄 Załadowano 3014 dokumentów.
k=2: Sil=0.477, CH=1360.9, DB=0.52
k=3: Sil=0.527, CH=1801.6, DB=0.85
k=4: Sil=0.575, CH=1637.0, DB=0.80
k=5: Sil=0.609, CH=1798.8, DB=1.11
k=6: Sil=0.610, CH=1559.3, DB=1.73
k=7: Sil=0.611, CH=1318.1, DB=1.80
k=8: Sil=0.584, CH=1176.5, DB=2.28
k=9: Sil=0.588, CH=1065.7, DB=2.20
k=10: Sil=0.586, CH=947.2, DB=2.01

✅ Best k based on Silhouette Score: 7

🏅 Top 5 PageRank: [(1928, 0.0004781667562776473), (2839, 0.00047569693100241086), (2153, 0.0004657644819264554), (2528, 0.0004657644819264554), (2752, 0.0004657183993256468)]

📊 Final Clustering (k=7): Sil=0.611, CH=1318.1, DB=1.80
C:\Users\Paulina\Desktop\mgr\sem3\crawler\p2\lsi_clustering_analysis.py:128: MatplotlibDeprecationWarning: The get_cmap function was deprecated in Matplotlib 3.7 and will be removed in 3.11. Use ``matplotlib.colormaps[name]`` or ``matplotlib.colormaps.get_cmap()`` or ``pyplot.get_cmap()`` instead.
  cmap = cm.get_cmap('tab10', len(unique_clusters))

📌 PageRank vs Clusters:
  Doc 1928: PageRank=0.0005, Cluster=4
  Doc 2839: PageRank=0.0005, Cluster=4
  Doc 2153: PageRank=0.0005, Cluster=4
  Doc 2528: PageRank=0.0005, Cluster=4
  Doc 2752: PageRank=0.0005, Cluster=4

📊 PageRank – średnie i top 3 w każdym klastrze:

🔹 Cluster 0:
   Średni PageRank: 0.000286, Maksymalny: 0.000407, Liczba dokumentów: 505
   Top 3 dokumenty:
     1. Doc 849 – PageRank: 0.000407
     2. Doc 987 – PageRank: 0.000407
     3. Doc 1444 – PageRank: 0.000407

🔹 Cluster 1:
   Średni PageRank: 0.000331, Maksymalny: 0.000331, Liczba dokumentów: 407
   Top 3 dokumenty:
     1. Doc 0 – PageRank: 0.000331
     2. Doc 2 – PageRank: 0.000331
     3. Doc 4 – PageRank: 0.000331

🔹 Cluster 2:
   Średni PageRank: 0.000448, Maksymalny: 0.000448, Liczba dokumentów: 1151
   Top 3 dokumenty:
     1. Doc 8 – PageRank: 0.000448
     2. Doc 10 – PageRank: 0.000448
     3. Doc 13 – PageRank: 0.000448

🔹 Cluster 3:
   Średni PageRank: 0.000196, Maksymalny: 0.000202, Liczba dokumentów: 146
   Top 3 dokumenty:
     1. Doc 1357 – PageRank: 0.000202
     2. Doc 71 – PageRank: 0.000201
     3. Doc 2958 – PageRank: 0.000201

🔹 Cluster 4:
   Średni PageRank: 0.000262, Maksymalny: 0.000478, Liczba dokumentów: 501
   Top 3 dokumenty:
     1. Doc 1928 – PageRank: 0.000478
     2. Doc 2839 – PageRank: 0.000476
     3. Doc 2153 – PageRank: 0.000466

🔹 Cluster 5:
   Średni PageRank: 0.000146, Maksymalny: 0.000224, Liczba dokumentów: 20
   Top 3 dokumenty:
     1. Doc 2793 – PageRank: 0.000224
     2. Doc 1300 – PageRank: 0.000223
     3. Doc 1036 – PageRank: 0.000223

🔹 Cluster 6:
   Średni PageRank: 0.000150, Maksymalny: 0.000253, Liczba dokumentów: 281
   Top 3 dokumenty:
     1. Doc 1651 – PageRank: 0.000253
     2. Doc 2964 – PageRank: 0.000249
     3. Doc 64 – PageRank: 0.000245

📈 Statystyki grafu podobieństw:
  Wierzchołki: 3011
  Krawędzie: 2197319
  Średni stopień: 1459.53
  Maksymalny stopień: 2220
  Składowe spójne: 1
  Największa składowa: 3011

Process finished with exit code 0
