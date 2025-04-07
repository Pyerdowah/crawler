import threading
from queue import Queue

import networkx as nx
from tqdm import tqdm

from downloader import download_page
from parser import extract_links
from robots import RobotsChecker


class AtomicCounter:
    def __init__(self, initial=0):
        self.value_ = initial
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value_ += 1

    def decrement(self):
        with self.lock:
            self.value_ -= 1

    def value(self):
        with self.lock:
            return self.value_


class WebCrawler:
    def __init__(self, base_url, max_pages=300, num_threads=10):
        self.base_url = base_url
        self.max_pages = max_pages
        self.num_threads = num_threads

        self.queue = Queue()
        self.visited = set()
        self.graph = nx.DiGraph()
        self.robots = RobotsChecker(base_url)

        self.lock = threading.Lock()
        self.cv = threading.Condition()

        self.total_visited = AtomicCounter(0)
        self.working_threads = AtomicCounter(0)
        self.pages_limit_reached = AtomicCounter(0)

        self.progress = tqdm(total=max_pages, desc="Crawling")

    def crawl(self):
        self.queue.put(self.base_url)
        self.run_crawler()
        self.progress.close()
        return self.graph

    def run_crawler(self):
        while True:
            if self.pages_limit_reached.value():
                if self.working_threads.value() < 5:
                    print("Page limit reached, and threads finished. Exiting.")
                    break
                else:
                    self.gotosleep()
            else:
                if self.working_threads.value() < self.num_threads and not self.queue.empty():
                    self.create_thread()
                elif self.working_threads.value() == 0:
                    print("No threads active and queue empty. Exiting.")
                    break
                else:
                    self.gotosleep()

    def create_thread(self):
        url = self.queue.get()
        self.working_threads.increment()

        t = threading.Thread(target=self.child_thread, args=(url,))
        t.start()

    def gotosleep(self):
        with self.cv:
            self.cv.wait()

    def awake(self):
        with self.cv:
            self.cv.notify()

    def child_thread(self, url):
        if not self.robots.can_fetch(url):
            self.working_threads.decrement()
            self.awake()
            return

        html = download_page(url)
        if html is None:
            self.working_threads.decrement()
            self.awake()
            return

        links = extract_links(self.base_url, html)

        with self.lock:
            if url not in self.visited:
                self.visited.add(url)
                self.total_visited.increment()
                self.progress.update(1)

                if self.total_visited.value() >= self.max_pages:
                    self.pages_limit_reached.increment()

            for link in links:
                if link not in self.visited:
                    self.queue.put(link)
                else:
                    self.graph.add_edge(url, link)

        self.working_threads.decrement()
        self.awake()
