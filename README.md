# Zadanie 1. Robot internetowy i graf WWW. (30 pkt)

1. Napisz robota internetowego, który przegląda zasoby w obrębie podanej (rozsądnie dużej, min. 3000 podstron) domeny należącej do **ZAGRANICZNEJ uczelni** i zapisuje na dysku kopie dokumentów oraz analizuje graf połączeń między nimi.

2. Wymagania:
   1. przestrzeganie ograniczeń Robots Exclusion Protocol (**2 pkt**)
   2. wielowątkowe ściąganie dokumentów z zastosowaniem kolejki zadań, analiza działania dla wielu wariantów uruchomienia z wieloma wątkami (m.in. pomiar czasów dla różnej liczby wątków) (**4 pkt**)
   3. analiza grafu połączeń między dokumentami (**18 pkt**):
      - liczba wierzchołków i łuków
      - analiza składowych spójności: słabe (WCC), silne (SCC), komponenty IN, OUT, graf SCC (podział na SCC)
      - rozkłady stopni (in, out), wyznaczenie współczynników funkcji potęgowej metodami analitycznymi (np. regresja)
      - najkrótsze ścieżki (wszystkie pary): średnia odległość, średnica grafu, promienie dla każdego wierzchołka, histogramy dla średnich odległości i analiza ich rozkładu (np. metoda regresji)
      - współczynniki klasteryzacji: lokalne oraz globalne (analiza histogramów i regresja dla rozkładów)
      - odporność na awarie i ataki: zmiany grafu przy usuwaniu wierzchołków losowych (awarie) oraz maksymalnego stopnia (ataki): analiza składowych spójności (analogicznie jak p.2), analiza rozkładów stopni (analogicznie jak p.3) oraz analiza odległości (analogicznie jak p.4)
      - spójność wierzchołkowa (również przy atakach i awariach): znalezienie wierzchołków rozspajających (jeżeli graf jest 1-spójny) albo par wierzchołków rozspajających (jeżeli graf jest 2-spójny)
   4. wyznacz rangi stron z zastosowaniem zaimplementowanego przez siebie iteracyjnego algorytmu PageRank (z tłumieniem i bez tłumienia), zbadaj rozkład wartości PageRank (w stosunku do rozkładu potęgowego), zbadaj zbieżność metody dla różnych wartości współczynnika tłumienia (**6 pkt**)

3. Obowiązkowe sprawozdanie! Sprawozdanie musi mieć formę pisemną, zawierać definicje, pojęcia i własności rozważanych zagadnień. Można wykorzystać chatAI.

4. Terminy:
   - Termin bonusowy (125% punktów): **29.04.2024**
   - Termin podstawowy (100% punktów): **16.05.2024**
   - Termin spóźniony (75% punktów): **06.06.2024**
   - Termin bardzo spóźniony (50% punktów): **27.09.2024**
