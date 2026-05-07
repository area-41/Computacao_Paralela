from concurrent.futures import ThreadPoolExecutor
import time
import random

def tarefa(n):
    tempo = random.randint(2, 4)
    time.sleep(tempo)
    return f"Tarefa {n} (durou {tempo}s)"

with ThreadPoolExecutor(max_workers=3) as executor:
    numeros = range(5)
    resultados = executor.map(tarefa, numeros)

    for resultado in resultados:
        print(resultado)