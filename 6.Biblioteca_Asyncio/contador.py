import asyncio
import time

async def cronometro():
    # Loop de 1 a 10 segundos para expor visualmente o tempo passando
    for segundo in range(1, 11):
        await asyncio.sleep(1)
        print(# Deslocado para a direita para não misturar com as outras mensagens
            f"[Cronômetro: {segundo}s]"
        )

async def olaMundo():
    print("Iniciou o processo 01...")
    await asyncio.sleep(7)
    print("Fim do processo 01!!!")

async def olaMundo2():
    print("Iniciou o processo 02...")
    await asyncio.sleep(3)
    print("Fim do processo 02!!!")

async def main():
    # Criamos a tarefa do cronômetro junto com as outras
    tarefa_tempo = asyncio.create_task(cronometro())
    tarefa1 = asyncio.create_task(olaMundo())
    tarefa2 = asyncio.create_task(olaMundo2())

    # Aguardamos todas as tarefas terminarem
    await tarefa1
    await tarefa2
    await tarefa_tempo

    print("Fim do main...")

if __name__ == '__main__':
    # Registra o tempo exato do início da execução
    inicio = time.time()
    
    asyncio.run(main())
    
    # Exibe o tempo total gasto pelo programa inteiro
    print(f"\nTempo total de execução do programa: {time.time() - inicio:.2f} segundos")