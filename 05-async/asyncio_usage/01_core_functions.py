# ============================================================
# 📘 asyncio Core Functions
# ============================================================

import asyncio
import time

# 1. asyncio.run() - 运行协程的主函数
# Knowledge:
# - Python 3.7+ 推荐使用
# - 自动创建和管理事件循环
# - 运行完成后自动关闭事件循环

async def hello_world():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# 使用 asyncio.run() 运行协程
def demo_run():
    print("=== asyncio.run() 示例 ===")
    asyncio.run(hello_world())

# 2. 事件循环管理
# Knowledge:
# - 手动管理事件循环
# - 适用于需要自定义循环的场景
# - 记得关闭循环

async def event_loop_demo():
    print("事件循环演示")
    await asyncio.sleep(0.5)

def demo_event_loop():
    print("=== 事件循环管理示例 ===")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(event_loop_demo())
    finally:
        loop.close()

# 3. 创建和运行任务
# Knowledge:
# - create_task() 创建任务
# - 任务可以并发执行
# - 可以取消和监控任务

async def worker(name, delay):
    print(f"Worker {name} 开始")
    await asyncio.sleep(delay)
    print(f"Worker {name} 完成")
    return f"Worker {name} 的结果"

async def demo_tasks():
    print("=== 任务管理示例 ===")
    
    # 创建任务
    task1 = asyncio.create_task(worker("A", 2))
    task2 = asyncio.create_task(worker("B", 1))
    
    # 等待所有任务完成
    results = await asyncio.gather(task1, task2)
    print(f"所有任务完成: {results}")

# 4. 并发执行
# Knowledge:
# - gather() 等待多个协程完成
# - 返回所有结果
# - 按输入顺序返回结果

async def demo_gather():
    print("=== 并发执行示例 ===")
    
    # 并发执行多个协程
    results = await asyncio.gather(
        worker("X", 1),
        worker("Y", 2),
        worker("Z", 3)
    )
    print(f"并发结果: {results}")

# 5. 等待第一个完成
# Knowledge:
# - wait() 等待任务完成
# - 可以设置等待条件
# - 返回完成和未完成的任务

async def demo_wait():
    print("=== 等待第一个完成示例 ===")
    
    tasks = [
        asyncio.create_task(worker("Fast", 1)),
        asyncio.create_task(worker("Slow", 3))
    ]
    
    # 等待第一个完成
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"完成的任务: {len(done)}")
    print(f"未完成的任务: {len(pending)}")
    
    # 取消未完成的任务
    for task in pending:
        task.cancel()

# 6. 超时控制
# Knowledge:
# - wait_for() 添加超时
# - 超时后抛出 TimeoutError
# - 可以捕获超时异常

async def slow_operation():
    print("开始慢操作")
    await asyncio.sleep(5)
    print("慢操作完成")
    return "操作成功"

async def demo_timeout():
    print("=== 超时控制示例 ===")
    
    try:
        # 设置3秒超时
        result = await asyncio.wait_for(slow_operation(), timeout=3)
        print(f"结果: {result}")
    except asyncio.TimeoutError:
        print("操作超时")

# 7. 取消任务
# Knowledge:
# - cancel() 取消任务
# - 被取消的任务会抛出 CancelledError
# - 可以检查任务是否被取消

async def cancellable_worker():
    try:
        print("开始可取消的工作")
        await asyncio.sleep(10)
        print("工作完成")
    except asyncio.CancelledError:
        print("工作被取消")
        raise

async def demo_cancel():
    print("=== 取消任务示例 ===")
    
    task = asyncio.create_task(cancellable_worker())
    
    # 等待1秒后取消
    await asyncio.sleep(1)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("任务已取消")

# 主函数
async def main():
    print("🚀 asyncio 核心函数演示")
    print("=" * 50)
    
    # 运行各种演示
    demo_run()
    print()
    
    demo_event_loop()
    print()
    
    await demo_tasks()
    print()
    
    await demo_gather()
    print()
    
    await demo_wait()
    print()
    
    await demo_timeout()
    print()
    
    await demo_cancel()
    print()
    
    print("✅ 所有演示完成")

if __name__ == "__main__":
    asyncio.run(main()) 