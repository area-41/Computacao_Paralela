import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


# --- TAREFAS ---

def tarefa_io_download(url):
    """Simula uma tarefa de I/O (Download de arquivos)."""
    try:
        resposta = requests.get(url, timeout=10)
        return f"Download concluído: {url} ({len(resposta.content)} bytes)"
    except Exception as e:
        return f"Erro em {url}: {e}"


def tarefa_cpu_primo(n):
    """Simula uma tarefa de CPU (Cálculo matemático pesado)."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def tarefa_simples_sleep(n):
    """Tarefa genérica para demonstrar ciclo de vida."""
    tempo = random.randint(1, 3)
    time.sleep(tempo)
    return f"Tarefa {n} finalizada em {tempo}s"


# --- EXECUÇÕES ---

def rodar_exemplo_io():
    print("\n=== 1. TESTE I/O-BOUND (ThreadPoolExecutor) ===")
    urls = ["https://httpbin.org/bytes/500000"] * 7
    inicio = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Usando map para manter a ordem
        resultados = executor.map(tarefa_io_download, urls)
        for res in resultados:
            print(res)

    print(f"Tempo total I/O: {time.time() - inicio:.2f}s")


def rodar_exemplo_cpu():
    print("\n=== 2. TESTE CPU-BOUND (ProcessPoolExecutor) ===")
    # Números grandes para forçar a CPU
    numeros = [122725350953003, 122725350953011, 122725350953053, 122725350953159]
    inicio = time.time()

    with ProcessPoolExecutor(max_workers=4) as executor:
        # Convertendo para lista para disparar a execução
        resultados = list(executor.map(tarefa_cpu_primo, numeros))
        print(f"Resultados (Primos): {resultados}")

    print(f"Tempo total CPU: {time.time() - inicio:.2f}s")


def rodar_exemplo_ciclo_vida():
    print("\n=== 3. CONTROLE DE CICLO DE VIDA (as_completed) ===")
    print("Iniciando 5 tarefas (máximo 3 simultâneas)...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        # submit() retorna um objeto Future imediatamente
        futures = {executor.submit(tarefa_simples_sleep, i): i for i in range(7)}

        # as_completed() libera o resultado assim que a tarefa termina
        for future in as_completed(futures):
            try:
                print(future.result())
            except Exception as e:
                print(f"Tarefa gerou exceção: {e}")


if __name__ == "__main__":
    print("Iniciando Laboratório de Computação Paralela...")

    rodar_exemplo_io()
    rodar_exemplo_cpu()
    rodar_exemplo_ciclo_vida()

    print("\nLaboratório concluído com sucesso.")
