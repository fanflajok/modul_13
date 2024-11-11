import asyncio
standings = 1
async def start_strongman(name, power):
    global standings
    sum_of_balls = 5
    print(f'Силач {name} начал соревнования')
    await asyncio.sleep(8 / power)
    for i in range(0, sum_of_balls):
        print(f'Силач {name} поднял {i+1} шар')
        await asyncio.sleep(8 / power)
    print(f'Силач {name} закончил соревнования и занял {standings} место')
    standings += 1


async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Wario', 3))
    task2 = asyncio.create_task(start_strongman('Ganon', 4))
    task3 = asyncio.create_task(start_strongman('Link', 5))
    await task1
    await task2
    await task3


asyncio.run(start_tournament())