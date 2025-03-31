import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import networkx as nx

from downloader import download_page
from parser import extract_links
from robots import RobotsChecker

class WebCrawler:
    def __init__(self, base_url, max_pages=30, num_threads=10):
        self.base_url = base_url
        self.visited = set()
        self.queue = Queue()
        self.lock = threading.Lock()
        self.max_pages = max_pages
        self.graph = nx.DiGraph()
        self.robots = RobotsChecker(base_url)
        self.num_threads = num_threads

    def crawl(self):
        self.queue.put(self.base_url)

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(self.worker) for _ in range(self.num_threads)]
            for future in futures:
                future.result()

        return self.graph

    def worker(self):
        while not self.queue.empty() and len(self.visited) < self.max_pages:
            url = self.queue.get()
            with self.lock:
                if url in self.visited:
                    continue
                self.visited.add(url)
            if not self.robots.can_fetch(url):
                continue

            html = download_page(url)
            if html is None:
                continue

            links = extract_links(self.base_url, html)
            with self.lock:
                for link in links:
                    self.graph.add_edge(url, link)
                    if link not in self.visited:
                        self.queue.put(link)
