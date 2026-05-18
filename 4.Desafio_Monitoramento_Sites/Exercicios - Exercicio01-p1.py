import threading
import requests   #Requisições HTTP
import time       #Capturar horários

parar_threads = threading.Event()

def isAlive(url, intervalTime):
    print(f"[INFO] Monitorando: {url}")

    while not parar_threads.is_set():
        try:
            requisicao = requests.get(url)

            if requisicao.status_code >= 400:
                print(f"[ALERTA] Site {url} está fora do ar! (tentativa em {time.ctime(time.time())})")
            elif requisicao.status_code == 200:
                print(f"[INFO]. Site {url} está ativo. (tentativa em {time.ctime(time.time())})")
            else:
                print(f"{requisicao.status_code}")

        except Exception as e:
            print(f"[ALERTA] Domínio não encontrado: {url} (tentativa em {time.ctime(time.time())})")

        time.sleep(intervalTime)

if __name__ == "__main__":

    urls = [
        "https://www.google.com",
        "https://www.terra.com.br",
        "https://naoexiste.com.fak",
        "https://httpstat.us/404"
    ]

    threads = []

    for url in urls:
        novaThread = threading.Thread(target=isAlive, args=(url, 2))
        threads.append(novaThread)
        novaThread.start()

    while True:
        comando = input().strip()

        if comando == "sair":
            parar_threads.set()

            for thread in threads:
                thread.join()
            
            print("Encerrando o monitoramento de sites...")
            break
            
        else:
            print("Digite 'sair' para finalizar o monitoramento.")

    
    
