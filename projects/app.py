import asyncio
from contextvars import ContextVar

async def count (counter):
    print(f"Колличество записей в списке: {len(counter)}")

    while True:
        await asyncio.sleep(1 / 1000)
        counter.append(1)


async def print_every_one_sec(counter):
    while True:
        await asyncio.sleep(1)
        print(f'- 1 секунда прошла. '
              f'Колличество записей в списке: {len(counter)}')


async def print_every_5_sec():
    while True:
        await asyncio.sleep(5)
        print(f'---- 5 секунд прошло.')


async def print_every_10_sec():
    while True:
        await asyncio.sleep(10)
        print(f'-------- 10 секунд прошло.')


async def main():
    counter = list()

    c = count(counter)
    p1 = print_every_one_sec(counter)
    p5 = print_every_5_sec()
    p10 = print_every_10_sec()

    asyncio.create_task(c)
    asyncio.create_task(p1)
    asyncio.create_task(p5)
    await p10


asyncio.run(main())