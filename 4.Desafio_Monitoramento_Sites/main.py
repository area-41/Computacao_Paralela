
"""
1.Lista de sites a monitorar
2.Uma thread para cada site da lista
3.Execução contínua (loop infinito)
4.Encerramento com segurança
"""
import requests, threading
from datetime import datetime


# 1.Lista de sites a monitorar
SITES = [
    "https://www.google.com/",
    "https://www.python.org/",
    "https://httpbin.org/status/404"  # Exemplo que retorna erro 404
]

# Evento global para sinalizar a parada de todas as threads
parar_monitoramento = threading.Event()

# 2.Uma thread para cada site da lista

def monitorar_site(url):
    print(f"[INFO] Monitorando: {url}")
    while not parar_monitoramento.is_set():
        try:
            # Faz a requisição com um timeout para evitar que a thread trave em sites lentos
            resposta = requests.get(url, timeout=7)

            # Se o status code for >= 400, considera fora do ar
            if resposta.status_code >= 400:
                # Captura a hora atual formatada para o alerta de status ruim
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"\n[ALERTA] Site {url} está FORA DO AR! (tentativa em {agora} {resposta.status_code})")
            else:
                # Opcional: log de sucesso para acompanhamento
                print(f"[INFO] Site {url} está OK.")
        except requests.RequestException:
            # Captura falhas de conexão, DNS inexistente, timeouts, etc.
            print(f"\n[ALERTA] {url} está INACESSÍVEL (Falha de Conexão/DNS)!")

            # 2. Espera 10 segundos antes da próxima checagem.
            # Usar parar_monitoramento.wait(10) é melhor que time.sleep(10) porque se o usuário
            # digitar 'sair', a thread interrompe a espera imediatamente em vez de esperar os 10s acabarem.
        parar_monitoramento.wait(10)

    print(f"[ENCERRADO] Thread de monitoramento de: {url}")


def main():
    threads = []

    # 2. Criando e iniciando uma thread para cada site
    for site in SITES:
        thread = threading.Thread(target=monitorar_site, args=(site,))
        thread.daemon = True  # Garante que as threads não travem o encerramento do script
        threads.append(thread)
        thread.start()

    # 4. Encerramento com segurança via console principal
    print("\n--- Monitor iniciado. Digite 'sair' a qualquer momento para encerrar. ---\n")
    while True:
        comando = input().strip().lower()
        if comando == 'sair':
            print("\nEncerrando monitoramento, aguarde as threads finalizarem...")
            # Ativa o evento para que todas as threads saiam do loop 'while'
            parar_monitoramento.set()
            break

    # Aguarda todas as threads terminarem a rodada atual antes de fechar o programa
    for thread in threads:
        thread.join()

    print("Programa encerrado com sucesso!")

if __name__ == "__main__":
    main()