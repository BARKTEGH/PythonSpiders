import requests
import urllib

import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

if __name__ == '__main__':
    proxies = []
    for i in range(10):
        proxies.append(get_proxy())
    print(proxies)