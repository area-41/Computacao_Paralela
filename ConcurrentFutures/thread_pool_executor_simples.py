from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def tarefa(n):
    time.sleep(1)
    return n * 10

if __name__ == '__main__':
    """Esse programa executa 5 tarefas simultaneamente, 
    no máximo 3 de cada vez no Thread Pool, retornando os resultados 
    à medida que cada uma é concluída."""
    with ThreadPoolExecutor(max_workers=3) as executor:
        # bloco with, executor encerra automaticamente threads ou processos
        futures = [executor.submit(tarefa, i) for i in range(5)]
        for future in as_completed(futures):
            print(f"Resultado: {future.result()} {tarefa}")
