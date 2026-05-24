import asyncio
import random

async def somar(x, y, tempo):
    print(f"Iniciou a soma de {x} + {y} com tempo de espera de {tempo} segundos")
    await asyncio.sleep(tempo)
    print(f"Acabou de aguardar {tempo} segundos")
    return x + y

async def main():
    # Dicionário dedicado para armazenar as tarefas assíncronas
    tasks_agendadas = {}
    
    for i in range(5):
        nome = f"task_{i}"
        
        # Cria Task e guarda no dicionário
        tasks_agendadas[nome] = asyncio.create_task(
            somar(random.randint(1, 100), random.randint(1, 100), random.randint(1, 5))
        )
    
    # Aguardar todas terminarem de forma eficiente com asyncio.gather
    resultados = await asyncio.gather(*tasks_agendadas.values())
    print("\nTodos os resultados:", resultados)
    for i, resultado in enumerate(resultados):
        print(f"Resultado obtido task {i}: {resultado}")


if __name__ == '__main__':

    asyncio.run(main())