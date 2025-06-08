# Coroutines


import asyncio


async def say_hello():
    print("Hello, world!")
    await asyncio.sleep(1)
    print("It's been 1 second")

coro = say_hello() # this will not wait for the asyncio.sleep(1) to finish

asyncio.run(coro)