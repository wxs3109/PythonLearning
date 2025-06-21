# ============================================================
# 📘 asyncio Synchronization Primitives
# ============================================================

import asyncio
import time

# 1. Lock - 异步锁
# Knowledge:
# - 确保同一时间只有一个协程访问资源
# - 防止竞态条件
# - 支持 async with 语法

async def worker_with_lock(name, lock):
    async with lock:
        print(f"Worker {name} 获得锁")
        await asyncio.sleep(1)  # 模拟工作
        print(f"Worker {name} 释放锁")

async def demo_lock():
    print("=== Lock 示例 ===")
    lock = asyncio.Lock()
    
    # 创建多个任务竞争锁
    tasks = [
        worker_with_lock(f"Task-{i}", lock)
        for i in range(3)
    ]
    
    await asyncio.gather(*tasks)

# 2. Semaphore - 信号量
# Knowledge:
# - 限制同时访问资源的协程数量
# - 控制并发度
# - 防止资源过载

async def worker_with_semaphore(name, semaphore):
    async with semaphore:
        print(f"Worker {name} 获得信号量")
        await asyncio.sleep(2)  # 模拟工作
        print(f"Worker {name} 释放信号量")

async def demo_semaphore():
    print("=== Semaphore 示例 ===")
    # 限制最多2个并发
    semaphore = asyncio.Semaphore(2)
    
    tasks = [
        worker_with_semaphore(f"Task-{i}", semaphore)
        for i in range(5)
    ]
    
    await asyncio.gather(*tasks)

# 3. Event - 事件
# Knowledge:
# - 用于协程间的通信
# - 一个协程设置事件，其他协程等待
# - 适合通知机制

async def event_setter(event):
    print("事件设置者开始")
    await asyncio.sleep(2)
    print("设置事件")
    event.set()

async def event_waiter(name, event):
    print(f"等待者 {name} 等待事件")
    await event.wait()
    print(f"等待者 {name} 收到事件")

async def demo_event():
    print("=== Event 示例 ===")
    event = asyncio.Event()
    
    # 创建等待者和设置者
    waiters = [
        event_waiter(f"Waiter-{i}", event)
        for i in range(3)
    ]
    
    setter = event_setter(event)
    
    # 同时运行
    await asyncio.gather(setter, *waiters)

# 4. Condition - 条件变量
# Knowledge:
# - 用于复杂的同步场景
# - 可以等待特定条件
# - 支持通知机制

async def producer(condition, queue):
    for i in range(3):
        await asyncio.sleep(1)
        async with condition:
            queue.append(f"Item-{i}")
            print(f"生产者添加 Item-{i}")
            condition.notify()  # 通知消费者

async def consumer(name, condition, queue):
    for _ in range(3):
        async with condition:
            while not queue:
                print(f"消费者 {name} 等待")
                await condition.wait()
            
            item = queue.pop(0)
            print(f"消费者 {name} 消费 {item}")

async def demo_condition():
    print("=== Condition 示例 ===")
    condition = asyncio.Condition()
    queue = []
    
    # 创建生产者和消费者
    producer_task = producer(condition, queue)
    consumer_tasks = [
        consumer(f"Consumer-{i}", condition, queue)
        for i in range(2)
    ]
    
    await asyncio.gather(producer_task, *consumer_tasks)

# 5. Barrier - 屏障
# Knowledge:
# - 等待指定数量的协程到达
# - 所有协程同时继续执行
# - 适合同步点

async def barrier_worker(name, barrier):
    print(f"Worker {name} 到达屏障")
    await barrier.wait()
    print(f"Worker {name} 通过屏障")

async def demo_barrier():
    print("=== Barrier 示例 ===")
    # 等待3个协程到达
    barrier = asyncio.Barrier(3)
    
    tasks = [
        barrier_worker(f"Task-{i}", barrier)
        for i in range(3)
    ]
    
    await asyncio.gather(*tasks)

# 6. Queue - 异步队列
# Knowledge:
# - 线程安全的队列
# - 支持生产者-消费者模式
# - 可以设置最大大小

async def producer_queue(queue):
    for i in range(5):
        await asyncio.sleep(0.5)
        await queue.put(f"Item-{i}")
        print(f"生产者放入 Item-{i}")

async def consumer_queue(name, queue):
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=3)
            print(f"消费者 {name} 消费 {item}")
            queue.task_done()
        except asyncio.TimeoutError:
            print(f"消费者 {name} 超时退出")
            break

async def demo_queue():
    print("=== Queue 示例 ===")
    queue = asyncio.Queue(maxsize=3)
    
    # 创建生产者和消费者
    producer_task = producer_queue(queue)
    consumer_tasks = [
        consumer_queue(f"Consumer-{i}", queue)
        for i in range(2)
    ]
    
    # 等待生产者完成
    await producer_task
    
    # 等待队列清空
    await queue.join()
    
    # 取消消费者
    for task in consumer_tasks:
        task.cancel()
    
    await asyncio.gather(*consumer_tasks, return_exceptions=True)

# 7. 实际应用示例 - 连接池
# Knowledge:
# - 使用信号量限制连接数
# - 模拟数据库连接池

class ConnectionPool:
    def __init__(self, max_connections=3):
        self.semaphore = asyncio.Semaphore(max_connections)
        self.active_connections = 0
    
    async def get_connection(self):
        async with self.semaphore:
            self.active_connections += 1
            print(f"获取连接，当前活跃连接: {self.active_connections}")
            return Connection(self)
    
    def release_connection(self):
        self.active_connections -= 1
        print(f"释放连接，当前活跃连接: {self.active_connections}")

class Connection:
    def __init__(self, pool):
        self.pool = pool
    
    async def execute(self, query):
        print(f"执行查询: {query}")
        await asyncio.sleep(1)  # 模拟查询时间
        return f"查询结果: {query}"
    
    async def close(self):
        self.pool.release_connection()

async def database_worker(name, pool):
    async with pool.get_connection() as conn:
        result = await conn.execute(f"SELECT * FROM users WHERE id = {name}")
        print(f"Worker {name}: {result}")

async def demo_connection_pool():
    print("=== 连接池示例 ===")
    pool = ConnectionPool(max_connections=2)
    
    tasks = [
        database_worker(f"Worker-{i}", pool)
        for i in range(5)
    ]
    
    await asyncio.gather(*tasks)

# 主函数
async def main():
    print("🔒 asyncio 同步原语演示")
    print("=" * 50)
    
    await demo_lock()
    print()
    
    await demo_semaphore()
    print()
    
    await demo_event()
    print()
    
    await demo_condition()
    print()
    
    await demo_barrier()
    print()
    
    await demo_queue()
    print()
    
    await demo_connection_pool()
    print()
    
    print("✅ 所有同步原语演示完成")

if __name__ == "__main__":
    asyncio.run(main()) 