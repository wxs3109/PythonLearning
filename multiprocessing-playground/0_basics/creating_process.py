# ============================================================
# 📘 创建和管理进程
# ============================================================

import multiprocessing as mp
import os
import time
import psutil

# 1. 基本进程创建
# Knowledge:
# - Process(target=func, args=(), kwargs={})
# - start() 启动进程
# - join() 等待进程完成
# - is_alive() 检查进程状态

def basic_worker(name, delay):
    """基本工作函数"""
    print(f"进程 {name} (PID: {os.getpid()}) 开始工作")
    time.sleep(delay)
    print(f"进程 {name} 完成工作")
    return f"{name} 的结果"

def demo_basic_process():
    print("=== 基本进程创建 ===")
    
    # 创建进程
    p1 = mp.Process(target=basic_worker, args=("Worker1", 2))
    p2 = mp.Process(target=basic_worker, args=("Worker2", 1))
    
    print("启动进程...")
    p1.start()
    p2.start()
    
    print(f"进程1状态: {'活跃' if p1.is_alive() else '已结束'}")
    print(f"进程2状态: {'活跃' if p2.is_alive() else '已结束'}")
    
    # 等待进程完成
    p1.join()
    p2.join()
    
    print("所有进程已完成")

# 2. 进程参数传递
# Knowledge:
# - args: 位置参数元组
# - kwargs: 关键字参数字典
# - 参数必须是可序列化的

def parameter_worker(name, age, city="Unknown"):
    """带参数的工作函数"""
    print(f"进程 {name}: 年龄 {age}, 城市 {city}")
    time.sleep(1)
    return f"{name} 的信息"

def demo_parameters():
    print("\n=== 进程参数传递 ===")
    
    # 位置参数
    p1 = mp.Process(target=parameter_worker, args=("Alice", 25))
    
    # 关键字参数
    p2 = mp.Process(target=parameter_worker, 
                   args=("Bob", 30), 
                   kwargs={"city": "Beijing"})
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()

# 3. 进程名称和PID
# Knowledge:
# - name: 进程名称
# - pid: 进程ID
# - 可以通过名称识别进程

def named_worker():
    """命名进程的工作函数"""
    current_process = mp.current_process()
    print(f"进程名称: {current_process.name}")
    print(f"进程PID: {current_process.pid}")
    print(f"父进程PID: {os.getppid()}")
    time.sleep(1)

def demo_named_processes():
    print("\n=== 命名进程 ===")
    
    processes = []
    for i in range(3):
        p = mp.Process(target=named_worker, name=f"Worker-{i}")
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

# 4. 进程状态管理
# Knowledge:
# - is_alive(): 检查进程是否运行
# - exitcode: 退出码
# - terminate(): 终止进程
# - kill(): 强制杀死进程

def long_running_worker():
    """长时间运行的进程"""
    print(f"进程 {os.getpid()} 开始长时间运行")
    try:
        for i in range(10):
            print(f"进程 {os.getpid()}: 第 {i+1} 秒")
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"进程 {os.getpid()} 被中断")

def demo_process_control():
    print("\n=== 进程控制 ===")
    
    p = mp.Process(target=long_running_worker)
    p.start()
    
    # 监控进程状态
    for i in range(3):
        time.sleep(1)
        print(f"进程状态: {'活跃' if p.is_alive() else '已结束'}")
        print(f"退出码: {p.exitcode}")
    
    # 终止进程
    print("终止进程...")
    p.terminate()
    p.join()
    
    print(f"最终退出码: {p.exitcode}")

# 5. 进程继承
# Knowledge:
# - 子进程继承父进程的部分资源
# - 环境变量、文件描述符等
# - 内存空间是独立的

def inheritance_worker():
    """测试进程继承"""
    print(f"子进程 PID: {os.getpid()}")
    print(f"父进程 PID: {os.getppid()}")
    print(f"环境变量 HOME: {os.environ.get('HOME', 'Not set')}")
    print(f"当前工作目录: {os.getcwd()}")

def demo_inheritance():
    print("\n=== 进程继承 ===")
    
    # 设置环境变量
    os.environ['CUSTOM_VAR'] = 'test_value'
    
    p = mp.Process(target=inheritance_worker)
    p.start()
    p.join()

# 6. 进程池 vs 单个进程
# Knowledge:
# - Pool: 管理多个进程
# - 自动负载均衡
# - 资源复用

def pool_worker(x):
    """池工作函数"""
    time.sleep(0.1)
    return x * x

def demo_pool_vs_single():
    print("\n=== 进程池 vs 单个进程 ===")
    
    data = list(range(10))
    
    # 使用进程池
    start_time = time.time()
    with mp.Pool(4) as pool:
        results = pool.map(pool_worker, data)
    pool_time = time.time() - start_time
    print(f"进程池耗时: {pool_time:.3f} 秒")
    
    # 使用单个进程
    start_time = time.time()
    processes = []
    results = []
    for item in data:
        p = mp.Process(target=lambda x, r: r.append(pool_worker(x)), 
                      args=(item, results))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    single_time = time.time() - start_time
    print(f"单个进程耗时: {single_time:.3f} 秒")
    
    print(f"进程池比单个进程快: {single_time/pool_time:.2f} 倍")

# 7. 进程监控
# Knowledge:
# - 使用 psutil 监控进程
# - 获取CPU和内存使用情况
# - 进程树结构

def monitoring_worker():
    """被监控的进程"""
    process = psutil.Process()
    print(f"进程 {os.getpid()} 开始")
    
    # 模拟CPU密集型工作
    for i in range(1000000):
        _ = i * i
    
    print(f"进程 {os.getpid()} 完成")

def demo_process_monitoring():
    print("\n=== 进程监控 ===")
    
    p = mp.Process(target=monitoring_worker)
    p.start()
    
    # 监控进程
    while p.is_alive():
        try:
            process = psutil.Process(p.pid)
            cpu_percent = process.cpu_percent()
            memory_info = process.memory_info()
            
            print(f"PID {p.pid}: CPU {cpu_percent:.1f}%, "
                  f"内存 {memory_info.rss/1024/1024:.1f}MB")
            
            time.sleep(0.5)
        except psutil.NoSuchProcess:
            break
    
    p.join()
    print("监控完成")

# 8. 错误处理
# Knowledge:
# - 进程异常处理
# - 超时机制
# - 优雅关闭

def error_worker(should_fail=False):
    """可能出错的进程"""
    if should_fail:
        raise ValueError("模拟错误")
    
    print(f"进程 {os.getpid()} 正常完成")
    return "成功"

def demo_error_handling():
    print("\n=== 错误处理 ===")
    
    # 正常进程
    p1 = mp.Process(target=error_worker, args=(False,))
    p1.start()
    p1.join()
    print(f"正常进程退出码: {p1.exitcode}")
    
    # 出错进程
    p2 = mp.Process(target=error_worker, args=(True,))
    p2.start()
    p2.join()
    print(f"出错进程退出码: {p2.exitcode}")

# 主函数
def main():
    print("🚀 进程创建和管理演示")
    print("=" * 50)
    
    demo_basic_process()
    demo_parameters()
    demo_named_processes()
    demo_process_control()
    demo_inheritance()
    demo_pool_vs_single()
    demo_process_monitoring()
    demo_error_handling()
    
    print("\n✅ 所有演示完成")

if __name__ == "__main__":
    main() 