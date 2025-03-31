import requests
import os
import hashlib

def download_page(url, save_dir="data/html"):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            os.makedirs(save_dir, exist_ok=True)
            filename = hashlib.md5(url.encode()).hexdigest() + ".html"
            path = os.path.join(save_dir, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            return response.text
    except requests.RequestException:
        pass
    return None
