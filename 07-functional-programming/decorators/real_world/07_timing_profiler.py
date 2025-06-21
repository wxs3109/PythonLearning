# ============================================================
# 📘 性能计时 / profile 装饰器
# ============================================================

import functools
import time
import cProfile
import pstats
import io
import statistics
from typing import Callable, Dict, List, Optional, Any
from collections import defaultdict
import threading

# 1. 基础计时装饰器
# Knowledge:
# - 使用 time.time() 和 time.perf_counter()
# - 记录函数执行时间
# - 简单的性能监控

def basic_timing_decorator(func: Callable) -> Callable:
    """基础计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        print(f"⏱️  {func.__name__} 执行时间: {execution_time:.6f} 秒")
        
        return result
    return wrapper

@basic_timing_decorator
def simple_function(n: int) -> int:
    """简单函数"""
    time.sleep(0.1)  # 模拟计算时间
    return sum(i for i in range(n))

def demo_basic_timing():
    print("=== 基础计时装饰器演示 ===")
    
    result = simple_function(1000)
    print(f"结果: {result}")

# 2. 统计计时装饰器
# Knowledge:
# - 收集多次调用的统计信息
# - 计算平均值、最大值、最小值
# - 性能趋势分析

def statistical_timing_decorator(func: Callable) -> Callable:
    """统计计时装饰器"""
    # 使用线程锁确保线程安全
    lock = threading.Lock()
    stats = {
        'calls': 0,
        'total_time': 0.0,
        'times': [],
        'min_time': float('inf'),
        'max_time': 0.0
    }
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        
        # 线程安全地更新统计信息
        with lock:
            stats['calls'] += 1
            stats['total_time'] += execution_time
            stats['times'].append(execution_time)
            stats['min_time'] = min(stats['min_time'], execution_time)
            stats['max_time'] = max(stats['max_time'], execution_time)
        
        return result
    
    # 添加统计信息访问方法
    def get_stats() -> Dict[str, Any]:
        with lock:
            if stats['calls'] == 0:
                return stats.copy()
            
            return {
                'calls': stats['calls'],
                'total_time': stats['total_time'],
                'avg_time': stats['total_time'] / stats['calls'],
                'min_time': stats['min_time'],
                'max_time': stats['max_time'],
                'median_time': statistics.median(stats['times']),
                'std_dev': statistics.stdev(stats['times']) if len(stats['times']) > 1 else 0
            }
    
    def reset_stats():
        with lock:
            stats['calls'] = 0
            stats['total_time'] = 0.0
            stats['times'].clear()
            stats['min_time'] = float('inf')
            stats['max_time'] = 0.0
    
    wrapper.get_stats = get_stats
    wrapper.reset_stats = reset_stats
    
    return wrapper

@statistical_timing_decorator
def variable_function(n: int) -> int:
    """执行时间可变的函数"""
    # 模拟不同的执行时间
    time.sleep(0.05 + (n % 3) * 0.1)
    return n * n

def demo_statistical_timing():
    print("\n=== 统计计时装饰器演示 ===")
    
    # 多次调用
    for i in range(5):
        result = variable_function(i)
        print(f"调用 {i+1}: 结果 = {result}")
    
    # 查看统计信息
    stats = variable_function.get_stats()
    print("\n统计信息:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.6f}")
        else:
            print(f"  {key}: {value}")

# 3. 阈值监控装饰器
# Knowledge:
# - 设置性能阈值
# - 自动告警机制
# - 性能退化检测

def threshold_monitoring_decorator(warning_threshold: float = 1.0, 
                                 error_threshold: float = 5.0) -> Callable:
    """阈值监控装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            
            # 检查阈值
            if execution_time >= error_threshold:
                print(f"🚨 严重警告: {func.__name__} 执行时间 {execution_time:.3f}s 超过错误阈值 {error_threshold}s")
            elif execution_time >= warning_threshold:
                print(f"⚠️  性能警告: {func.__name__} 执行时间 {execution_time:.3f}s 超过警告阈值 {warning_threshold}s")
            else:
                print(f"✅ 性能正常: {func.__name__} 执行时间 {execution_time:.3f}s")
            
            return result
        return wrapper
    return decorator

@threshold_monitoring_decorator(warning_threshold=0.5, error_threshold=1.0)
def monitored_function(n: int) -> int:
    """被监控的函数"""
    time.sleep(0.6)  # 超过警告阈值
    return n * 2

def demo_threshold_monitoring():
    print("\n=== 阈值监控装饰器演示 ===")
    
    result = monitored_function(10)
    print(f"结果: {result}")

# 4. 内存监控装饰器
# Knowledge:
# - 监控内存使用情况
# - 内存泄漏检测
# - 内存效率分析

def memory_monitoring_decorator(func: Callable) -> Callable:
    """内存监控装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 获取初始内存使用
        start_memory = get_memory_usage()
        
        result = func(*args, **kwargs)
        
        # 获取结束内存使用
        end_memory = get_memory_usage()
        memory_used = end_memory - start_memory
        
        print(f"💾 {func.__name__} 内存使用: {memory_used} KB")
        
        if memory_used > 1024:  # 1MB
            print(f"⚠️  内存警告: {func.__name__} 使用了 {memory_used/1024:.2f} MB")
        
        return result
    return wrapper

def get_memory_usage() -> int:
    """获取当前内存使用（KB）"""
    import os
    import psutil
    try:
        process = psutil.Process(os.getpid())
        return process.memory_info().rss // 1024
    except ImportError:
        return 0

@memory_monitoring_decorator
def memory_intensive_function(n: int) -> List[int]:
    """内存密集型函数"""
    return [i * i for i in range(n)]

def demo_memory_monitoring():
    print("\n=== 内存监控装饰器演示 ===")
    
    result = memory_intensive_function(10000)
    print(f"生成了 {len(result)} 个数字")

# 5. cProfile 装饰器
# Knowledge:
# - 使用 cProfile 进行详细分析
# - 生成性能报告
# - 函数调用分析

def cprofile_decorator(func: Callable) -> Callable:
    """cProfile 装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 创建 profiler
        profiler = cProfile.Profile()
        
        # 开始分析
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        # 生成报告
        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        stats.print_stats(10)  # 显示前10个函数
        
        print(f"📊 {func.__name__} 性能分析:")
        print(s.getvalue())
        
        return result
    return wrapper

@cprofile_decorator
def complex_function(n: int) -> int:
    """复杂函数"""
    result = 0
    for i in range(n):
        for j in range(i):
            result += j
    return result

def demo_cprofile():
    print("\n=== cProfile 装饰器演示 ===")
    
    result = complex_function(100)
    print(f"结果: {result}")

# 6. 性能比较装饰器
# Knowledge:
# - 比较不同实现的性能
# - A/B 测试
# - 性能基准测试

def performance_comparison_decorator(baseline_func: Callable) -> Callable:
    """性能比较装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 测试基准函数
            start_time = time.perf_counter()
            baseline_result = baseline_func(*args, **kwargs)
            baseline_time = time.perf_counter() - start_time
            
            # 测试目标函数
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            target_time = time.perf_counter() - start_time
            
            # 比较性能
            if target_time < baseline_time:
                improvement = ((baseline_time - target_time) / baseline_time) * 100
                print(f"🚀 {func.__name__} 比 {baseline_func.__name__} 快 {improvement:.1f}%")
            else:
                slowdown = ((target_time - baseline_time) / baseline_time) * 100
                print(f"🐌 {func.__name__} 比 {baseline_func.__name__} 慢 {slowdown:.1f}%")
            
            print(f"  基准函数: {baseline_time:.6f}s")
            print(f"  目标函数: {target_time:.6f}s")
            
            return result
        return wrapper
    return decorator

def baseline_fibonacci(n: int) -> int:
    """基准斐波那契实现"""
    if n <= 1:
        return n
    return baseline_fibonacci(n-1) + baseline_fibonacci(n-2)

@performance_comparison_decorator(baseline_fibonacci)
def optimized_fibonacci(n: int) -> int:
    """优化的斐波那契实现"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def demo_performance_comparison():
    print("\n=== 性能比较装饰器演示 ===")
    
    result = optimized_fibonacci(30)
    print(f"结果: {result}")

# 7. 异步性能监控装饰器
# Knowledge:
# - 监控异步函数性能
# - 异步上下文管理
# - 协程性能分析

import asyncio

def async_timing_decorator(func: Callable) -> Callable:
    """异步计时装饰器"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        print(f"⏱️  异步函数 {func.__name__} 执行时间: {execution_time:.6f} 秒")
        
        return result
    return wrapper

@async_timing_decorator
async def async_function(n: int) -> int:
    """异步函数"""
    await asyncio.sleep(0.1)  # 模拟异步操作
    return n * 2

async def demo_async_timing():
    print("\n=== 异步计时装饰器演示 ===")
    
    result = await async_function(10)
    print(f"结果: {result}")

# 8. 性能报告生成器
# Knowledge:
# - 生成详细的性能报告
# - 数据可视化准备
# - 性能趋势分析

class PerformanceReporter:
    """性能报告生成器"""
    
    def __init__(self):
        self.reports = defaultdict(list)
    
    def timing_decorator(self, category: str = "default"):
        """带分类的计时装饰器"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                
                execution_time = end_time - start_time
                
                # 记录性能数据
                self.reports[category].append({
                    'function': func.__name__,
                    'execution_time': execution_time,
                    'timestamp': time.time(),
                    'args': str(args),
                    'kwargs': str(kwargs)
                })
                
                return result
            return wrapper
        return decorator
    
    def generate_report(self) -> Dict[str, Any]:
        """生成性能报告"""
        report = {}
        
        for category, data in self.reports.items():
            if not data:
                continue
            
            times = [item['execution_time'] for item in data]
            report[category] = {
                'total_calls': len(data),
                'total_time': sum(times),
                'avg_time': statistics.mean(times),
                'min_time': min(times),
                'max_time': max(times),
                'median_time': statistics.median(times),
                'std_dev': statistics.stdev(times) if len(times) > 1 else 0
            }
        
        return report
    
    def print_report(self):
        """打印性能报告"""
        report = self.generate_report()
        
        print("\n📊 性能报告:")
        print("=" * 50)
        
        for category, stats in report.items():
            print(f"\n分类: {category}")
            print(f"  总调用次数: {stats['total_calls']}")
            print(f"  总执行时间: {stats['total_time']:.6f}s")
            print(f"  平均执行时间: {stats['avg_time']:.6f}s")
            print(f"  最小执行时间: {stats['min_time']:.6f}s")
            print(f"  最大执行时间: {stats['max_time']:.6f}s")
            print(f"  中位数执行时间: {stats['median_time']:.6f}s")
            print(f"  标准差: {stats['std_dev']:.6f}s")

# 使用性能报告生成器
reporter = PerformanceReporter()

@reporter.timing_decorator("database")
def database_query(query: str) -> List[Dict]:
    """数据库查询"""
    time.sleep(0.2)
    return [{"id": 1, "name": "test"}]

@reporter.timing_decorator("api")
def api_call(endpoint: str) -> Dict:
    """API调用"""
    time.sleep(0.1)
    return {"status": "success"}

@reporter.timing_decorator("computation")
def heavy_computation(n: int) -> int:
    """重计算"""
    time.sleep(0.3)
    return sum(i * i for i in range(n))

def demo_performance_reporter():
    print("\n=== 性能报告生成器演示 ===")
    
    # 执行各种操作
    database_query("SELECT * FROM users")
    api_call("/api/users")
    heavy_computation(1000)
    
    database_query("SELECT * FROM orders")
    api_call("/api/orders")
    heavy_computation(500)
    
    # 生成报告
    reporter.print_report()

# 主函数
def main():
    print("⏱️  性能计时装饰器演示")
    print("=" * 50)
    
    demo_basic_timing()
    demo_statistical_timing()
    demo_threshold_monitoring()
    demo_memory_monitoring()
    demo_cprofile()
    demo_performance_comparison()
    
    # 运行异步演示
    asyncio.run(demo_async_timing())
    
    demo_performance_reporter()
    
    print("\n✅ 性能计时装饰器演示完成")

if __name__ == "__main__":
    main() 