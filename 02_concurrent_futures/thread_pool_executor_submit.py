from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random


def tarefa(n):
    tempo = time.sleep(random.randint(2, 5))
    return f"Tarefa {n} (duração de {tempo}s) completa"


with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(tarefa, i) for i in range(5)]

    for future in as_completed(futures):
        print(future.result())