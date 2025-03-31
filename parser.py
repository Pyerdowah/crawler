from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_links(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        joined = urljoin(base_url, href)
        if urlparse(joined).netloc == urlparse(base_url).netloc:
            links.add(joined.split('#')[0])  # usuwanie kotwic
    return links
