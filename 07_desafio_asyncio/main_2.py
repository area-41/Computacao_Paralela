import asyncio
import csv
from datetime import datetime
import os
import time
import aiohttp

# Configurações
URLS = [
    "https://www.google.com",
    "https://www.github.com",
    "https://httpstat.us/200",
    "https://httpstat.us/503",
    "https://httpstat.us/404",
]
CSV_FILE = "status.csv"
INTERVALO_SEGUNDOS = 60
TIMEOUT_REQUISICAO = 10  # Tempo limite para cada URL responder


async def verificar_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Verifica uma única URL de forma assíncrona e mede o tempo de resposta."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = time.perf_counter()

    try:
        # Define um timeout individual para a requisição
        timeout = aiohttp.ClientTimeout(total=TIMEOUT_REQUISICAO)
        async with session.get(url, timeout=timeout) as response:
            # Força a leitura do conteúdo para garantir que a resposta foi totalmente recebida
            await response.read()
            elapsed = time.perf_counter() - start_time
            return {
                "timestamp": timestamp,
                "url": url,
                "status_code": response.status,
                "response_time": f"{elapsed:.3f}",
            }
    except Exception:
        # Captura timeouts, erros de conexão, DNS, etc.
        elapsed = time.perf_counter() - start_time
        return {
            "timestamp": timestamp,
            "url": url,
            "status_code": "ERROR",
            "response_time": f"{elapsed:.3f}",
        }


async def rodar_rodada_monitoramento():
    """Gerencia uma rodada de verificação de todas as URLs em paralelo."""
    # Cria o arquivo CSV com o cabeçalho caso ele não exista
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "url", "status_code", "response_time"])

    # Executa as requisições concorrentemente
    async with aiohttp.ClientSession() as session:
        tasks = [verificar_url(session, url) for url in URLS]
        resultados = await asyncio.gather(*tasks)

    # Salva os resultados no CSV
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for res in resultados:
            writer.writerow(
                [
                    res["timestamp"],
                    res["url"],
                    res["status_code"],
                    res["response_time"],
                ]
            )

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checkpoint salvo em '{CSV_FILE}'")


async def main():
    print("Iniciando o monitoramento... Pressione Ctrl+C para encerrar.")
    try:
        while True:
            start_loop = time.time()

            # Executa o bloco de monitoramento assíncrono
            await rodar_rodada_monitoramento()

            # Calcula quanto tempo a execução demorou para compensar o sleep
            # Garantindo que o loop aconteça rigidamente a cada 60 segundos
            tempo_gasto = time.time() - start_loop
            proximo_sleep = max(0.0, INTERVALO_SEGUNDOS - tempo_gasto)

            await asyncio.sleep(proximo_sleep)

    except asyncio.CancelledError:
        print("\nMonitoramento cancelado.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário (Ctrl+C).")