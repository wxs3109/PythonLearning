# async_await.py

import asyncio
import time  # Only used to show why blocking is bad


# ============================================================
# ⚙️ Introduction to async/await
# ------------------------------------------------------------
# - async/await is used for asynchronous programming in Python
# - It allows non-blocking execution of tasks like I/O operations
# - Requires Python 3.5+
# - Use asyncio module for managing async tasks
# ============================================================

async def say_hello():
    print("Hello, world!")
    await asyncio.sleep(1)
    print("It's been 1 second")

asyncio.run(say_hello())


# ============================================================
# 🧪 Define a basic async function
# ------------------------------------------------------------
# - Already shown above with say_hello()
# ============================================================


# ============================================================
# ⏳ Running multiple async tasks concurrently
# ------------------------------------------------------------
# - Create two async functions with different delays
# - Use asyncio.gather() to run them at the same time
# - Demonstrate that total runtime is less than the sum of delays
# ============================================================

async def slow_task():
    print("Slow task started")
    await asyncio.sleep(10)
    print("Slow task finished")

async def fast_task():
    print("Fast task started")
    await asyncio.sleep(5)
    print("Fast task finished")

async def run_gather_example():
    await asyncio.gather(slow_task(), fast_task())

asyncio.run(run_gather_example())  # Expected total time: ~10 seconds


# ============================================================
# 🧵 asyncio.create_task()
# ------------------------------------------------------------
# - Use asyncio.create_task() to schedule coroutines ahead of time
# - Show that tasks can run independently and finish in any order
# ============================================================

async def run_create_task_example():
    task1 = asyncio.create_task(slow_task())
    task2 = asyncio.create_task(fast_task())
    await task1
    await task2

asyncio.run(run_create_task_example())


# ============================================================
# ⚠️ Awaiting blocking code (what not to do)
# ------------------------------------------------------------
# - Demonstrate that using time.sleep() inside async functions blocks everything
# - Explain that only await-compatible functions (like asyncio.sleep) should be awaited
# ============================================================

# ❌ BAD: This will block the event loop, defeating the purpose of async
async def fast_task_blocking():
    print("Fast task started")
    time.sleep(5)  # ⚠️ This blocks the entire event loop
    print("Fast task finished")

async def run_with_blocking_code():
    await asyncio.gather(slow_task(), fast_task_blocking())

# Commented out to avoid blocking your terminal
# asyncio.run(run_with_blocking_code())


# ============================================================
# 🔁 async for / async with
# ------------------------------------------------------------
# - Create an async generator and use 'async for' to iterate over it
# - Use 'async with' for an asynchronous context manager
# ============================================================

# Async generator
async def async_counter():
    for i in range(3):
        await asyncio.sleep(1)
        yield i

async def use_async_for():
    async for value in async_counter():
        print("Counter:", value)

asyncio.run(use_async_for())

# Async context manager (example with dummy class)
class AsyncContextExample:
    async def __aenter__(self):
        print("Entering async context")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Exiting async context")

    async def do_work(self):
        print("Doing async work...")
        await asyncio.sleep(1)

async def use_async_with():
    async with AsyncContextExample() as worker:
        await worker.do_work()

asyncio.run(use_async_with())


# ============================================================
# 💡 Real-world examples (optional)
# ------------------------------------------------------------
# - Simulate API calls using async functions
# - Show how async improves performance
# ============================================================

async def fake_api_call(name, delay):
    print(f"Calling API: {name}")
    await asyncio.sleep(delay)
    print(f"Response from {name}")

async def simulate_real_world():
    await asyncio.gather(
        fake_api_call("UserService", 2),
        fake_api_call("PaymentService", 3),
        fake_api_call("NotificationService", 1),
    )

asyncio.run(simulate_real_world())
