import asyncio
import random  # <-- CORRIGIDO: Importando o módulo completo

async def somar(x, y, tempo):
    print(f"Iniciou a soma de {x} + {y} com tempo de espera de {tempo:.2f} segundos")
    await asyncio.sleep(tempo)
    print(f"Acabou de aguardar {tempo:.2f} segundos")
    return x + y

async def main():
    # 1. Dicionário dedicado para armazenar suas tarefas assíncronas
    tasks_agendadas = {}
    
    for i in range(21):
        nome = f"task_{i}"
        
        # 2. Criar a task e guardar no dicionário
        tasks_agendadas[nome] = asyncio.create_task(
            somar(random.randint(1, 100), random.randint(1, 100), random.uniform(1, 5))
        )
    
    # 3. Aguardar todas terminarem de forma eficiente com asyncio.gather
    resultados = await asyncio.gather(*tasks_agendadas.values())
    
    print("\n--- Resultados Finais ---")
    for nome, resultado in zip(tasks_agendadas.keys(), resultados):
        print(f"{nome}: {resultado}")
    
    print("\nProcessamento concluído\n")
    print(f"Resultados obtidos: {resultados}")
    print(f"\nResultados obtidos (formatados com nome e índice): {[f'{nome}: {res:.2f}' for i, (nome, res) in enumerate(zip(tasks_agendadas.keys(), resultados))]}")


if __name__ == '__main__':
    asyncio.run(main())