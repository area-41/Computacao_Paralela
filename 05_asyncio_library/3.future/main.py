import asyncio

async def esperar_botao(futuro):
    print("Aguardando a inserção da entrada...")
    resultado = await futuro
    print(f"Finalmente o botão foi pressionado: {resultado}")

async def simular_pressionar_botao(futuro):
    await asyncio.sleep(7)
    botao_pressionado = 'R'
    futuro.set_result(botao_pressionado)

async def tarefa_secundaria():
    for i in range(5):
        print(f"Tarefa secundária sendo executada: passo {i+1}")
        await asyncio.sleep(1)

async def main():
    futuro = asyncio.Future()

    tarefa1 = asyncio.create_task(esperar_botao(futuro))
    tarefa2 = asyncio.create_task(simular_pressionar_botao(futuro))
    tarefa3 = asyncio.create_task(tarefa_secundaria())

    await asyncio.gather(tarefa1, tarefa2, tarefa3)


if __name__ == '__main__':
    asyncio.run(main())