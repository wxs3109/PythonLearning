# ============================================================
# 📘 缓存（memoization）示例
# ============================================================

import functools
import time
import hashlib
import pickle
import json
from typing import Any, Callable, Dict, Optional, Union
from collections import OrderedDict
import threading

# 1. 基础缓存装饰器
# Knowledge:
# - 使用字典存储函数结果
# - 基于参数创建缓存键
# - 避免重复计算

def basic_cache_decorator(func: Callable) -> Callable:
    """基础缓存装饰器"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 创建缓存键
        key = str((args, sorted(kwargs.items())))
        
        # 检查缓存
        if key in cache:
            print(f"💾 缓存命中: {func.__name__}")
            return cache[key]
        
        # 执行函数并缓存结果
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"💾 缓存存储: {func.__name__}")
        
        return result
    
    return wrapper

@basic_cache_decorator
def fibonacci(n: int) -> int:
    """斐波那契数列（递归实现）"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def demo_basic_cache():
    print("=== 基础缓存装饰器演示 ===")
    
    # 第一次调用（计算）
    result1 = fibonacci(10)
    print(f"fibonacci(10) = {result1}")
    
    # 第二次调用（从缓存获取）
    result2 = fibonacci(10)
    print(f"fibonacci(10) = {result2}")

# 2. LRU 缓存装饰器
# Knowledge:
# - 最近最少使用策略
# - 限制缓存大小
# - 自动淘汰旧条目

def lru_cache_decorator(maxsize: int = 128) -> Callable:
    """LRU 缓存装饰器"""
    def decorator(func: Callable) -> Callable:
        cache = OrderedDict()
        lock = threading.Lock()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = str((args, sorted(kwargs.items())))
            
            with lock:
                # 检查缓存
                if key in cache:
                    # 移动到末尾（最近使用）
                    cache.move_to_end(key)
                    print(f"💾 LRU缓存命中: {func.__name__}")
                    return cache[key]
                
                # 执行函数
                result = func(*args, **kwargs)
                
                # 存储到缓存
                cache[key] = result
                cache.move_to_end(key)
                
                # 检查缓存大小
                if len(cache) > maxsize:
                    # 删除最旧的条目
                    oldest_key = next(iter(cache))
                    del cache[oldest_key]
                    print(f"🗑️  LRU缓存淘汰: {oldest_key}")
                
                print(f"💾 LRU缓存存储: {func.__name__}")
                return result
        
        return wrapper
    return decorator

@lru_cache_decorator(maxsize=3)
def expensive_calculation(n: int) -> int:
    """昂贵的计算"""
    print(f"执行昂贵计算: {n}")
    time.sleep(0.1)  # 模拟计算时间
    return n * n

def demo_lru_cache():
    print("\n=== LRU 缓存装饰器演示 ===")
    
    # 填充缓存
    expensive_calculation(1)
    expensive_calculation(2)
    expensive_calculation(3)
    
    # 触发淘汰
    expensive_calculation(4)
    
    # 再次访问（应该从缓存获取）
    expensive_calculation(2)

# 3. TTL 缓存装饰器
# Knowledge:
# - 基于时间的缓存过期
# - 自动清理过期条目
# - 生存时间管理

def ttl_cache_decorator(ttl: float = 60.0) -> Callable:
    """TTL 缓存装饰器"""
    def decorator(func: Callable) -> Callable:
        cache = {}
        timestamps = {}
        lock = threading.Lock()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            key = str((args, sorted(kwargs.items())))
            
            with lock:
                # 检查缓存和过期时间
                if key in cache:
                    if current_time - timestamps[key] < ttl:
                        print(f"💾 TTL缓存命中: {func.__name__}")
                        return cache[key]
                    else:
                        # 删除过期条目
                        del cache[key]
                        del timestamps[key]
                        print(f"⏰ TTL缓存过期: {func.__name__}")
                
                # 执行函数
                result = func(*args, **kwargs)
                
                # 存储到缓存
                cache[key] = result
                timestamps[key] = current_time
                print(f"💾 TTL缓存存储: {func.__name__}")
                
                return result
        
        return wrapper
    return decorator

@ttl_cache_decorator(ttl=2.0)  # 2秒过期
def time_sensitive_function(n: int) -> str:
    """时间敏感函数"""
    print(f"执行时间敏感计算: {n}")
    return f"结果_{n}_{int(time.time())}"

def demo_ttl_cache():
    print("\n=== TTL 缓存装饰器演示 ===")
    
    # 第一次调用
    result1 = time_sensitive_function(5)
    print(f"结果: {result1}")
    
    # 立即再次调用（应该从缓存获取）
    result2 = time_sensitive_function(5)
    print(f"结果: {result2}")
    
    # 等待过期
    print("等待缓存过期...")
    time.sleep(3)
    
    # 过期后调用（重新计算）
    result3 = time_sensitive_function(5)
    print(f"结果: {result3}")

# 4. 智能缓存键生成器
# Knowledge:
# - 处理不可哈希参数
# - 对象序列化
# - 缓存键优化

def smart_cache_decorator(func: Callable) -> Callable:
    """智能缓存装饰器"""
    cache = {}
    
    def create_cache_key(*args, **kwargs) -> str:
        """创建智能缓存键"""
        try:
            # 尝试直接哈希
            key_data = (args, tuple(sorted(kwargs.items())))
            return str(hash(key_data))
        except TypeError:
            # 如果不可哈希，使用序列化
            try:
                # 尝试JSON序列化
                key_data = {
                    'args': args,
                    'kwargs': kwargs
                }
                return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
            except (TypeError, ValueError):
                # 最后使用pickle序列化
                key_data = (args, kwargs)
                return hashlib.md5(pickle.dumps(key_data)).hexdigest()
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = create_cache_key(*args, **kwargs)
        
        if key in cache:
            print(f"💾 智能缓存命中: {func.__name__}")
            return cache[key]
        
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"💾 智能缓存存储: {func.__name__}")
        
        return result
    
    return wrapper

@smart_cache_decorator
def complex_function(data: list, config: dict) -> list:
    """复杂函数（处理不可哈希参数）"""
    print(f"处理复杂数据: {len(data)} 项")
    return [x * 2 for x in data]

def demo_smart_cache():
    print("\n=== 智能缓存装饰器演示 ===")
    
    data1 = [1, 2, 3]
    config1 = {"mode": "fast"}
    
    # 第一次调用
    result1 = complex_function(data1, config1)
    print(f"结果: {result1}")
    
    # 第二次调用（应该从缓存获取）
    result2 = complex_function(data1, config1)
    print(f"结果: {result2}")

# 5. 分层缓存装饰器
# Knowledge:
# - 多级缓存策略
# - 内存和磁盘缓存
# - 缓存层次结构

class LayeredCache:
    """分层缓存系统"""
    
    def __init__(self, memory_size: int = 100, disk_enabled: bool = False):
        self.memory_cache = OrderedDict()
        self.memory_size = memory_size
        self.disk_enabled = disk_enabled
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """从缓存获取值"""
        with self.lock:
            # 检查内存缓存
            if key in self.memory_cache:
                self.memory_cache.move_to_end(key)
                print(f"💾 内存缓存命中: {key}")
                return self.memory_cache[key]
            
            # 检查磁盘缓存
            if self.disk_enabled:
                try:
                    disk_key = f"cache_{hashlib.md5(key.encode()).hexdigest()}"
                    with open(f"/tmp/{disk_key}.cache", 'rb') as f:
                        result = pickle.load(f)
                        print(f"💾 磁盘缓存命中: {key}")
                        return result
                except (FileNotFoundError, pickle.PickleError):
                    pass
            
            return None
    
    def set(self, key: str, value: Any):
        """设置缓存值"""
        with self.lock:
            # 存储到内存缓存
            self.memory_cache[key] = value
            self.memory_cache.move_to_end(key)
            
            # 检查内存缓存大小
            if len(self.memory_cache) > self.memory_size:
                oldest_key = next(iter(self.memory_cache))
                oldest_value = self.memory_cache[oldest_key]
                del self.memory_cache[oldest_key]
                
                # 移动到磁盘缓存
                if self.disk_enabled:
                    try:
                        disk_key = f"cache_{hashlib.md5(oldest_key.encode()).hexdigest()}"
                        with open(f"/tmp/{disk_key}.cache", 'wb') as f:
                            pickle.dump(oldest_value, f)
                        print(f"💾 移动到磁盘缓存: {oldest_key}")
                    except Exception as e:
                        print(f"❌ 磁盘缓存失败: {e}")

def layered_cache_decorator(memory_size: int = 100, disk_enabled: bool = False) -> Callable:
    """分层缓存装饰器"""
    cache = LayeredCache(memory_size, disk_enabled)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str((args, sorted(kwargs.items())))
            
            # 尝试从缓存获取
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存储到缓存
            cache.set(key, result)
            print(f"💾 分层缓存存储: {func.__name__}")
            
            return result
        
        return wrapper
    return decorator

@layered_cache_decorator(memory_size=2, disk_enabled=False)
def layered_function(n: int) -> int:
    """分层缓存函数"""
    print(f"执行分层计算: {n}")
    time.sleep(0.1)
    return n * n * n

def demo_layered_cache():
    print("\n=== 分层缓存装饰器演示 ===")
    
    # 填充内存缓存
    layered_function(1)
    layered_function(2)
    
    # 触发内存缓存淘汰
    layered_function(3)
    
    # 再次访问（应该从缓存获取）
    layered_function(1)

# 6. 条件缓存装饰器
# Knowledge:
# - 基于条件的缓存策略
# - 动态缓存控制
# - 缓存策略选择

def conditional_cache_decorator(condition_func: Callable = None) -> Callable:
    """条件缓存装饰器"""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 检查是否应该缓存
            should_cache = True
            if condition_func:
                should_cache = condition_func(*args, **kwargs)
            
            if not should_cache:
                print(f"🚫 跳过缓存: {func.__name__}")
                return func(*args, **kwargs)
            
            # 创建缓存键
            key = str((args, sorted(kwargs.items())))
            
            # 检查缓存
            if key in cache:
                print(f"💾 条件缓存命中: {func.__name__}")
                return cache[key]
            
            # 执行函数
            result = func(*args, **kwargs)
            cache[key] = result
            print(f"💾 条件缓存存储: {func.__name__}")
            
            return result
        
        return wrapper
    return decorator

def cache_condition(*args, **kwargs) -> bool:
    """缓存条件函数"""
    # 只缓存偶数参数
    if args and isinstance(args[0], int):
        return args[0] % 2 == 0
    return True

@conditional_cache_decorator(cache_condition)
def conditional_function(n: int) -> str:
    """条件缓存函数"""
    print(f"执行条件计算: {n}")
    return f"结果_{n}"

def demo_conditional_cache():
    print("\n=== 条件缓存装饰器演示 ===")
    
    # 偶数（应该缓存）
    result1 = conditional_function(2)
    result2 = conditional_function(2)
    
    # 奇数（不应该缓存）
    result3 = conditional_function(3)
    result4 = conditional_function(3)

# 7. 缓存统计装饰器
# Knowledge:
# - 缓存命中率统计
# - 性能分析
# - 缓存效果评估

def cache_stats_decorator(func: Callable) -> Callable:
    """缓存统计装饰器"""
    cache = {}
    stats = {
        'hits': 0,
        'misses': 0,
        'total_calls': 0
    }
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stats['total_calls'] += 1
        key = str((args, sorted(kwargs.items())))
        
        if key in cache:
            stats['hits'] += 1
            print(f"💾 缓存命中: {func.__name__}")
            return cache[key]
        
        stats['misses'] += 1
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"💾 缓存存储: {func.__name__}")
        
        return result
    
    def get_stats() -> Dict[str, Any]:
        """获取缓存统计信息"""
        hit_rate = stats['hits'] / stats['total_calls'] if stats['total_calls'] > 0 else 0
        return {
            'hits': stats['hits'],
            'misses': stats['misses'],
            'total_calls': stats['total_calls'],
            'hit_rate': hit_rate,
            'cache_size': len(cache)
        }
    
    def reset_stats():
        """重置统计信息"""
        stats['hits'] = 0
        stats['misses'] = 0
        stats['total_calls'] = 0
        cache.clear()
    
    wrapper.get_stats = get_stats
    wrapper.reset_stats = reset_stats
    
    return wrapper

@cache_stats_decorator
def stats_function(n: int) -> int:
    """统计缓存函数"""
    print(f"执行统计计算: {n}")
    time.sleep(0.05)
    return n * n

def demo_cache_stats():
    print("\n=== 缓存统计装饰器演示 ===")
    
    # 多次调用
    for i in range(5):
        stats_function(i)
    
    # 重复调用（应该命中缓存）
    for i in range(3):
        stats_function(i)
    
    # 查看统计信息
    stats = stats_function.get_stats()
    print("\n缓存统计:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2%}" if key == 'hit_rate' else f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")

# 8. 缓存预热装饰器
# Knowledge:
# - 预加载常用数据
# - 启动时优化
# - 缓存策略规划

def cache_warmup_decorator(preload_data: list) -> Callable:
    """缓存预热装饰器"""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        # 预热缓存
        print("🔥 开始缓存预热...")
        for item in preload_data:
            key = str((item,))
            result = func(item)
            cache[key] = result
            print(f"🔥 预热缓存: {func.__name__}({item})")
        print("🔥 缓存预热完成")
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str((args, sorted(kwargs.items())))
            
            if key in cache:
                print(f"💾 预热缓存命中: {func.__name__}")
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            print(f"💾 预热缓存存储: {func.__name__}")
            
            return result
        
        return wrapper
    return decorator

@cache_warmup_decorator([1, 2, 3, 4, 5])
def warmup_function(n: int) -> int:
    """缓存预热函数"""
    print(f"执行预热计算: {n}")
    time.sleep(0.1)
    return n * n

def demo_cache_warmup():
    print("\n=== 缓存预热装饰器演示 ===")
    
    # 预热的数据应该直接命中
    result1 = warmup_function(3)
    print(f"预热数据结果: {result1}")
    
    # 新数据需要计算
    result2 = warmup_function(10)
    print(f"新数据结果: {result2}")

# 主函数
def main():
    print("💾 缓存装饰器演示")
    print("=" * 50)
    
    demo_basic_cache()
    demo_lru_cache()
    demo_ttl_cache()
    demo_smart_cache()
    demo_layered_cache()
    demo_conditional_cache()
    demo_cache_stats()
    demo_cache_warmup()
    
    print("\n✅ 缓存装饰器演示完成")

if __name__ == "__main__":
    main() 