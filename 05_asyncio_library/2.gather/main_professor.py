import asyncio

async def somar(x, y, tempo):
    await asyncio.sleep(tempo)
    print(f"Acabou de aguardar {tempo} segundos")
    return x + y



async def main():
    task1 = asyncio.create_task(somar(10, 20, 10))
    task2 = asyncio.create_task(somar(50, 100, 2))
    task3 = asyncio.create_task(somar(50, 100, 2))
    task4 = asyncio.create_task(somar(2, 20, 10))
    task5 = asyncio.create_task(somar(15, 100, 2))
    task6 = asyncio.create_task(somar(6, 100, 2))

    resultados = await asyncio.gather(task1, task2, task3, task4, task5, task6)

    print(resultados)


    # resultado_1 = await task1
    # resultado_2 = await task2
    # resultado_3 = await task3
    # resultado_4 = await task4
    # resultado_5 = await task5
    # resultado_6 = await task6
    

    # print(f"Resultado 1: {resultado_1}")
    # print(f"Resultado 2: {resultado_2}")
    # print(f"Resultado 3: {resultado_3}")
    # print(f"Resultado 4: {resultado_4}")
    # print(f"Resultado 5: {resultado_5}")
    # print(f"Resultado 6: {resultado_6}")

if __name__ == '__main__':

    asyncio.run(main())