from crawler import WebCrawler

def build_graph(base_url, max_pages=3000, num_threads=10):
    crawler = WebCrawler(base_url, max_pages=max_pages, num_threads=num_threads)
    graph = crawler.crawl()
    return graph
