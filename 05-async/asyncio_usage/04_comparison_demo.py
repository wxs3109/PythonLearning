# ============================================================
# 📘 asyncio.sleep vs time.sleep vs asyncio.wait 对比
# ============================================================

import asyncio
import time

# 1. asyncio.sleep vs time.sleep 对比
# Knowledge:
# - asyncio.sleep 是非阻塞的，让出控制权
# - time.sleep 是阻塞的，会阻塞整个线程
# - 在协程中应该使用 asyncio.sleep

async def worker_async(name, delay):
    print(f"Worker {name} 开始")
    await asyncio.sleep(delay)  # 非阻塞
    print(f"Worker {name} 完成")
    return f"{name} 的结果"

def worker_sync(name, delay):
    print(f"Worker {name} 开始")
    time.sleep(delay)  # 阻塞
    print(f"Worker {name} 完成")
    return f"{name} 的结果"

async def demo_sleep_comparison():
    print("=== asyncio.sleep vs time.sleep 对比 ===")
    
    print("\n1. 使用 asyncio.sleep (非阻塞):")
    start = time.time()
    
    # 并发执行，总时间约2秒
    tasks = [
        worker_async("A", 2),
        worker_async("B", 2),
        worker_async("C", 2)
    ]
    results = await asyncio.gather(*tasks)
    
    end = time.time()
    print(f"asyncio.sleep 总时间: {end - start:.2f} 秒")
    print(f"结果: {results}")
    
    print("\n2. 使用 time.sleep (阻塞):")
    start = time.time()
    
    # 顺序执行，总时间约6秒
    results = []
    for name in ["A", "B", "C"]:
        result = worker_sync(name, 2)
        results.append(result)
    
    end = time.time()
    print(f"time.sleep 总时间: {end - start:.2f} 秒")
    print(f"结果: {results}")

# 2. asyncio.wait vs asyncio.gather 对比
# Knowledge:
# - wait 返回 (done, pending) 元组
# - gather 返回结果列表
# - wait 更灵活，gather 更简洁

async def demo_wait_vs_gather():
    print("\n=== asyncio.wait vs asyncio.gather 对比 ===")
    
    # 创建任务
    tasks = [
        asyncio.create_task(worker_async("Fast", 1)),
        asyncio.create_task(worker_async("Medium", 2)),
        asyncio.create_task(worker_async("Slow", 3))
    ]
    
    print("\n1. 使用 asyncio.wait (等待第一个完成):")
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"完成的任务数: {len(done)}")
    print(f"未完成的任务数: {len(pending)}")
    
    # 取消未完成的任务
    for task in pending:
        task.cancel()
    
    # 等待取消完成
    await asyncio.gather(*pending, return_exceptions=True)
    
    print("\n2. 使用 asyncio.gather (等待所有完成):")
    results = await asyncio.gather(
        worker_async("X", 1),
        worker_async("Y", 2),
        worker_async("Z", 3)
    )
    print(f"所有结果: {results}")

# 3. 错误处理对比
# Knowledge:
# - wait 需要手动处理异常
# - gather 可以自动处理异常

async def failing_worker(name):
    print(f"Worker {name} 开始")
    await asyncio.sleep(1)
    if name == "Error":
        raise ValueError(f"Worker {name} 出错了")
    print(f"Worker {name} 完成")
    return f"{name} 成功"

async def demo_error_handling():
    print("\n=== 错误处理对比 ===")
    
    print("\n1. asyncio.wait 错误处理:")
    tasks = [
        asyncio.create_task(failing_worker("OK")),
        asyncio.create_task(failing_worker("Error")),
        asyncio.create_task(failing_worker("OK2"))
    ]
    
    try:
        done, pending = await asyncio.wait(tasks)
        
        # 手动检查异常
        for task in done:
            try:
                result = task.result()
                print(f"成功: {result}")
            except Exception as e:
                print(f"失败: {e}")
        
        # 取消未完成的任务
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
        
    except Exception as e:
        print(f"等待出错: {e}")
    
    print("\n2. asyncio.gather 错误处理:")
    try:
        results = await asyncio.gather(
            failing_worker("OK"),
            failing_worker("Error"),
            failing_worker("OK2"),
            return_exceptions=True  # 返回异常而不是抛出
        )
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"任务 {i} 失败: {result}")
            else:
                print(f"任务 {i} 成功: {result}")
                
    except Exception as e:
        print(f"Gather 出错: {e}")

# 4. 性能对比
# Knowledge:
# - 测量不同方法的性能
# - 理解并发 vs 顺序执行

async def performance_test():
    print("\n=== 性能对比测试 ===")
    
    async def async_worker(i):
        await asyncio.sleep(0.1)
        return i
    
    # 测试 gather
    start = time.time()
    results = await asyncio.gather(*[async_worker(i) for i in range(10)])
    gather_time = time.time() - start
    
    # 测试 wait
    start = time.time()
    tasks = [asyncio.create_task(async_worker(i)) for i in range(10)]
    done, pending = await asyncio.wait(tasks)
    wait_time = time.time() - start
    
    print(f"gather 时间: {gather_time:.4f} 秒")
    print(f"wait 时间: {wait_time:.4f} 秒")
    print(f"gather 结果: {results}")
    print(f"wait 完成数: {len(done)}")

# 5. 实际应用场景
# Knowledge:
# - 何时使用 sleep
# - 何时使用 wait vs gather

async def real_world_examples():
    print("\n=== 实际应用场景 ===")
    
    print("\n1. 超时控制 (使用 wait_for):")
    try:
        result = await asyncio.wait_for(
            worker_async("Timeout", 5),
            timeout=2
        )
        print(f"结果: {result}")
    except asyncio.TimeoutError:
        print("操作超时")
    
    print("\n2. 并发下载 (使用 gather):")
    urls = ["url1", "url2", "url3"]
    async def download(url):
        await asyncio.sleep(1)  # 模拟下载
        return f"下载完成: {url}"
    
    results = await asyncio.gather(*[download(url) for url in urls])
    print(f"下载结果: {results}")
    
    print("\n3. 竞速模式 (使用 wait):")
    async def race_worker(name, delay):
        await asyncio.sleep(delay)
        return f"{name} 获胜"
    
    tasks = [
        asyncio.create_task(race_worker("兔子", 1)),
        asyncio.create_task(race_worker("乌龟", 3))
    ]
    
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    winner = list(done)[0]
    print(f"获胜者: {await winner}")
    
    # 取消其他任务
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)

# 主函数
async def main():
    print("🔄 asyncio 函数对比演示")
    print("=" * 60)
    
    await demo_sleep_comparison()
    await demo_wait_vs_gather()
    await demo_error_handling()
    await performance_test()
    await real_world_examples()
    
    print("\n✅ 所有对比演示完成")

if __name__ == "__main__":
    asyncio.run(main()) 