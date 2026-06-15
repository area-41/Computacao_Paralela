import threading
import requests    #Requisições HTTP
import time        #Capturar horários
from tabulate import tabulate

parar_threads = threading.Event()

STATUS_AGUARDANDO = "Aguardando..."
STATUS_ATIVO = "Ativo"
STATUS_INATIVO = "Inativo"
STATUS_NAO_ENCONTRADO = "Domínio não encontrado"

urls = [
    {"url": " https://www.google.com", "status": STATUS_AGUARDANDO},
    {"url": "https://www.terra.com.br", "status": STATUS_AGUARDANDO},
    {"url": "https://naoexiste.com.fak", "status": STATUS_AGUARDANDO},
    {"url": "https://httpstat.us/404", "status": STATUS_AGUARDANDO},
    {"url": "https://www.uol.com.br", "status": STATUS_AGUARDANDO},
]



def show_status():
    while not parar_threads.is_set():
        print("\033[2J\033[H", end='') #Limpar a minha tela
        print(f"Atualizado em: {time.ctime()}")
        print(tabulate(urls, headers={"url": "Domínio", "status": "Status"}, tablefmt="grid"))
        time.sleep(1)



def isAlive(url, intervalTime):
    print(f"[INFO] Monitorando: {url}")

    while not parar_threads.is_set():
        try:
            requisicao = requests.get(url['url'])
            
            if requisicao.status_code == 200:
                url["status"] = STATUS_ATIVO
            else:
                url["status"] = STATUS_INATIVO
        except:
            url["status"] = STATUS_NAO_ENCONTRADO

        time.sleep(intervalTime)


if __name__ == "__main__":

    threads = []

    for url in urls:
        novaThread = threading.Thread(target=isAlive, args=(url, 2))
        threads.append(novaThread)
        novaThread.start()

    t_status = threading.Thread(target=show_status)
    threads.append(t_status)
    t_status.start()

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
