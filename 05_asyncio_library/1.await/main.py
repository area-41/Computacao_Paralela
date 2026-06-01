import asyncio


async def somar(x, y, tempo):
    await asyncio.sleep(tempo)
    print(f"Acabou de aguardar {tempo} segundos")
    return x + y

async def main():
    task1 = asyncio.create_task(somar(10, 20, 10))
    task2 = asyncio.create_task(somar(50, 100, 2))

    resultado_1 = await task1
    resultado_2 = await task2

    print(f"Resultado 1: {resultado_1}")
    print(f"Resultado 2: {resultado_2}")


if __name__ == '__main__':
    asyncio.run(main())