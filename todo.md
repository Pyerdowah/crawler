   3. analiza grafu połączeń między dokumentami (**18 pkt**):
      - analiza składowych spójności: słabe (WCC), silne (SCC), komponenty IN, OUT, graf SCC (podział na SCC)
      - rozkłady stopni (in, out), wyznaczenie współczynników funkcji potęgowej metodami analitycznymi (np. regresja)
      - najkrótsze ścieżki (wszystkie pary): średnia odległość, średnica grafu, promienie dla każdego wierzchołka, histogramy dla średnich odległości i analiza ich rozkładu (np. metoda regresji)
      - współczynniki klasteryzacji: lokalne oraz globalne (analiza histogramów i regresja dla rozkładów)
      - odporność na awarie i ataki: zmiany grafu przy usuwaniu wierzchołków losowych (awarie) oraz maksymalnego stopnia (ataki): analiza składowych spójności (analogicznie jak p.2), analiza rozkładów stopni (analogicznie jak p.3) oraz analiza odległości (analogicznie jak p.4)
      - spójność wierzchołkowa (również przy atakach i awariach): znalezienie wierzchołków rozspajających (jeżeli graf jest 1-spójny) albo par wierzchołków rozspajających (jeżeli graf jest 2-spójny)
   4. wyznacz rangi stron z zastosowaniem zaimplementowanego przez siebie iteracyjnego algorytmu PageRank (z tłumieniem i bez tłumienia), zbadaj rozkład wartości PageRank (w stosunku do rozkładu potęgowego), zbadaj zbieżność metody dla różnych wartości współczynnika tłumienia (**6 pkt**)
