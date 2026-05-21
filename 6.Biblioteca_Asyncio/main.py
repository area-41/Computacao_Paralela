import asyncio

async def olaMundo():
    print("Olá Mundo!")
    await asyncio.sleep(5)
    print("Fim!!!")

async def olaMundo2():
    print("Olá Mundo 2!")
    await asyncio.sleep(2)
    print("Fim do Olá Mundo 2!")

async def main():
    tarefa1 = asyncio.create_task(olaMundo())
    tarefa2 = asyncio.create_task(olaMundo2())

    await tarefa1
    await tarefa2

    print("Fim do main...")

if __name__ == '__main__':
    asyncio.run(main())