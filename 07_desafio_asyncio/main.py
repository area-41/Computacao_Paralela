import asyncio
import csv
from datetime import datetime
import aiohttp

URLS = [
    "https://www.google.com",
    "https://www.python.org",
    "https://httpstat.us/503",
    "https://httpstat.us/200?sleep=2000",
    "https://thisurldoesnotexist.tld"
]

async def verificar_url(session, url):
    inicio = datetime.now()

    try:
        response = await session.get(url, timeout=5)

        try:
            duracao = (datetime.now() - inicio).total_seconds()
            return (datetime.now(), url, response.status, f"{duracao:.3f}")
        finally:
            await response.release()
    except Exception as e:
        duracao = (datetime.now() - inicio).total_seconds()
        return (datetime.now(), url, "ERROR", f"{duracao:.3f}")


async def monitorar():
    try:
        arquivo = open("status.csv", mode="w", newline="")
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {e}")
        return
    
    writer = csv.writer(arquivo)
    writer.writerow(["timestamp", "url", "status_code", "response_time"])

    session = None

    try:
        session = aiohttp.ClientSession()

        while True:
            tarefas = []

            for url in URLS:
                tarefa = verificar_url(session, url)
                tarefas.append(tarefa)

            resultados = await asyncio.gather(*tarefas) #[resultado_t1, resultado_t2...]

            print(resultados)

            for linha in resultados:
                writer.writerow([linha[0].strftime("%Y-%m-%d %H:%M:%S"), linha[1], linha[2], linha[3]])
                print(f"{linha[0]} | {linha[1]} | {linha[2]} | {linha[3]}s")

            await asyncio.sleep(3)

    except Exception as e:
            print(f"Erro durante o monitoramento: {e}")
    finally:
        if session:
            await session.close()
        arquivo.close()


if __name__ == '__main__':
    try:
        asyncio.run(monitorar())
    except KeyboardInterrupt:
        print("Monitoramento encerrado...")