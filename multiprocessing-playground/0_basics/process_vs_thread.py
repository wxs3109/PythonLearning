# ============================================================
# 📘 进程 vs 线程对比
# ============================================================

import multiprocessing as mp
import threading
import time
import os
import psutil

# 1. 基本概念对比
# Knowledge:
# - 进程: 独立内存空间，适合CPU密集型任务
# - 线程: 共享内存空间，适合I/O密集型任务
# - 进程开销大，线程开销小

def cpu_bound_task(n):
    """CPU密集型任务：计算斐波那契数列"""
    result = 0
    for i in range(n):
        result += i * i
    return result

def io_bound_task(n):
    """I/O密集型任务：模拟文件读写"""
    time.sleep(0.1)  # 模拟I/O操作
    return f"Task {n} completed"

# 2. 进程 vs 线程性能对比
def compare_performance():
    print("=== 进程 vs 线程性能对比 ===")
    
    # CPU密集型任务测试
    print("\n1. CPU密集型任务 (计算密集型):")
    
    # 使用进程
    start_time = time.time()
    with mp.Pool(4) as pool:
        results = pool.map(cpu_bound_task, [1000000] * 4)
    process_time = time.time() - start_time
    print(f"进程池耗时: {process_time:.2f} 秒")
    
    # 使用线程
    start_time = time.time()
    threads = []
    results = []
    for i in range(4):
        thread = threading.Thread(target=lambda: results.append(cpu_bound_task(1000000)))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    thread_time = time.time() - start_time
    print(f"线程池耗时: {thread_time:.2f} 秒")
    
    print(f"进程比线程快: {thread_time/process_time:.2f} 倍")
    
    # I/O密集型任务测试
    print("\n2. I/O密集型任务:")
    
    # 使用进程
    start_time = time.time()
    with mp.Pool(4) as pool:
        results = pool.map(io_bound_task, range(10))
    process_time = time.time() - start_time
    print(f"进程池耗时: {process_time:.2f} 秒")
    
    # 使用线程
    start_time = time.time()
    threads = []
    results = []
    for i in range(10):
        thread = threading.Thread(target=lambda x=i: results.append(io_bound_task(x)))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    thread_time = time.time() - start_time
    print(f"线程池耗时: {thread_time:.2f} 秒")
    
    print(f"线程比进程快: {process_time/thread_time:.2f} 倍")

# 3. 内存使用对比
def compare_memory_usage():
    print("\n=== 内存使用对比 ===")
    
    # 获取当前进程内存使用
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"初始内存使用: {initial_memory:.2f} MB")
    
    # 创建多个进程
    print("\n创建4个进程:")
    processes = []
    for i in range(4):
        p = mp.Process(target=lambda: time.sleep(1))
        processes.append(p)
        p.start()
    
    # 等待进程完成
    for p in processes:
        p.join()
    
    process_memory = process.memory_info().rss / 1024 / 1024
    print(f"进程后内存使用: {process_memory:.2f} MB")
    print(f"进程内存增加: {process_memory - initial_memory:.2f} MB")
    
    # 创建多个线程
    print("\n创建4个线程:")
    threads = []
    for i in range(4):
        t = threading.Thread(target=lambda: time.sleep(1))
        threads.append(t)
        t.start()
    
    # 等待线程完成
    for t in threads:
        t.join()
    
    thread_memory = process.memory_info().rss / 1024 / 1024
    print(f"线程后内存使用: {thread_memory:.2f} MB")
    print(f"线程内存增加: {thread_memory - process_memory:.2f} MB")

# 4. 共享数据对比
def compare_data_sharing():
    print("\n=== 数据共享对比 ===")
    
    # 线程间共享数据
    print("1. 线程间共享数据:")
    shared_data = [0]
    
    def thread_worker():
        shared_data[0] += 1
        print(f"线程 {threading.current_thread().name}: {shared_data[0]}")
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=thread_worker)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"最终结果: {shared_data[0]}")
    
    # 进程间共享数据
    print("\n2. 进程间共享数据:")
    manager = mp.Manager()
    shared_list = manager.list([0])
    
    def process_worker():
        shared_list[0] += 1
        print(f"进程 {os.getpid()}: {shared_list[0]}")
    
    processes = []
    for i in range(3):
        p = mp.Process(target=process_worker)
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print(f"最终结果: {shared_list[0]}")

# 5. 实际应用场景
def real_world_examples():
    print("\n=== 实际应用场景 ===")
    
    print("1. 适合使用进程的场景:")
    print("   - 图像处理")
    print("   - 科学计算")
    print("   - 机器学习训练")
    print("   - 加密解密")
    
    print("\n2. 适合使用线程的场景:")
    print("   - Web服务器")
    print("   - 数据库连接池")
    print("   - GUI应用程序")
    print("   - 文件下载器")

# 6. 选择指南
def selection_guide():
    print("\n=== 选择指南 ===")
    
    print("选择进程当:")
    print("✅ 任务计算密集")
    print("✅ 需要利用多核CPU")
    print("✅ 任务相对独立")
    print("✅ 内存充足")
    
    print("\n选择线程当:")
    print("✅ 任务I/O密集")
    print("✅ 需要共享数据")
    print("✅ 任务间需要通信")
    print("✅ 内存有限")

# 主函数
def main():
    print("🔄 进程 vs 线程对比演示")
    print("=" * 50)
    
    compare_performance()
    compare_memory_usage()
    compare_data_sharing()
    real_world_examples()
    selection_guide()
    
    print("\n✅ 对比演示完成")

if __name__ == "__main__":
    main() 