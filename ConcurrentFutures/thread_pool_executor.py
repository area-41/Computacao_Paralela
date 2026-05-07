import requests
from concurrent.futures import ThreadPoolExecutor
import time


def baixar(url):
    print(f"Iniciando o download: {url}")
    resposta = requests.get(url)
    print(f"O download terminou: {url}")
    return f"{url}: {len(resposta.content)} bytes"


if __name__ == '__main__':
    urls = [
        "https://httpbin.org/bytes/1000000",
        "https://httpbin.org/bytes/1000000",
        "https://httpbin.org/bytes/1000000",
        "https://httpbin.org/bytes/1000000",
        "https://httpbin.org/bytes/1000000",
        "https://httpbin.org/bytes/1000000",
        "https://httpbin.org/bytes/1000000",
        "https://httpbin.org/bytes/1000000",
    ]

    print("=== VERSÃO SEQUENCIAL ====")
    start_time = time.time()
    for i in urls:
        print(baixar(i))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"O tempo sequencial foi {elapsed_time} segundos")

    print(f"=== VERSÃO CONCORRENTE ===")
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        for resultado in executor.map(baixar, urls):
            print(resultado)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"O tempo da versão concorrente foi {elapsed_time} segundos")
