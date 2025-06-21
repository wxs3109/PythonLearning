# ============================================================
# 📘 Basic Async/Await Concepts
# ============================================================

import asyncio
import time

# 1. Basic Async Function
# Knowledge: 
# - async def creates a coroutine function
# - await pauses execution until the awaited coroutine completes
# - Coroutines must be run in an event loop
async def basic_async_function():
    # Your code here
    print("Basic async function started")
    await asyncio.sleep(1)
    print("Basic async function finished")

# 2. Async Sleep
# Knowledge:
# - asyncio.sleep() is non-blocking
# - Allows other tasks to run during the sleep
async def async_sleep_demo():
    # Your code here
    print("Async sleep demo started")
    await asyncio.sleep(1)
    print("Async sleep demo finished")

# 3. Running Multiple Coroutines
# Knowledge:
# - asyncio.gather() runs multiple coroutines concurrently
# - Returns results in the same order as input
async def run_multiple_tasks():
    # Your code here
    print("Running multiple tasks started")
    await asyncio.gather(
        basic_async_function(),
        async_sleep_demo()
    )
    print("Running multiple tasks finished")

# 4. Async with Timeout
# Knowledge:
# - asyncio.wait_for() adds timeout to coroutines
# - Raises TimeoutError if coroutine takes too long
async def async_with_timeout():
    # Your code here
    print("Async with timeout startfed")
    try:
        await asyncio.wait_for(basic_async_function(), timeout=0.5)
    except asyncio.TimeoutError:
        print("Async with timeout timed out")
    print("Async with timeout finished")

# 5. Async Context Manager
# Knowledge:
# - async with for async context managers
# - __aenter__ and __aexit__ methods
class AsyncResource:
    async def __aenter__(self):
        # Your code here
        pass
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Your code here
        pass

# Example usage
async def main():
    # Your code here
    pass

if __name__ == "__main__":
    asyncio.run(main()) 