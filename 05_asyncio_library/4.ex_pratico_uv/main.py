import requests
import asyncio
import time

def buscar_dados(url, futuro):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        futuro.set_result(resposta.content)
    except Exception as e:
        futuro.set_exception(e)


async def aguardar_resultado(futuro):
    try:
        dados = await futuro
        print(f"Dados coletados com sucesso")
        return dados[:200]
    except Exception as e:
        print(f"Erro ao baixar o conteúdo: {e}")
        return None

async def main():
    loop = asyncio.get_event_loop()

    url = "https://www.uol.com.br"

    futuro = asyncio.Future()

    loop.call_soon_threadsafe(buscar_dados, url, futuro)
    task = asyncio.create_task(aguardar_resultado(futuro))

    resultado = await task

    print("Processamento concluído")

    if resultado:
        print(f"Resultado --> {resultado}")


if __name__ == '__main__':
    time_inicio = time.time()
    asyncio.run(main())
    time_fim = time.time()
    print(f"Tempo total de execução: {time_fim - time_inicio:.2f} segundos")