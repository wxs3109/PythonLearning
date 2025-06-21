# ============================================================
# 📘 带参数的装饰器工厂（@decorator(arg)）
# ============================================================

import functools
import time
import random

# 1. 装饰器工厂的基本概念
# Knowledge:
# - 装饰器工厂是一个函数，返回装饰器
# - 允许在装饰时传入参数
# - 语法：@decorator_factory(arg1, arg2)
# - 等价于：func = decorator_factory(arg1, arg2)(func)

def decorator_factory(prefix="[INFO]"):
    """装饰器工厂：根据参数创建不同的装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{prefix} 调用函数: {func.__name__}")
            result = func(*args, **kwargs)
            print(f"{prefix} 函数 {func.__name__} 完成")
            return result
        return wrapper
    return decorator

@decorator_factory("[DEBUG]")
def debug_function():
    print("调试函数执行")

@decorator_factory("[ERROR]")
def error_function():
    print("错误函数执行")

def demo_decorator_factory():
    print("=== 装饰器工厂基本用法 ===")
    
    debug_function()
    print()
    error_function()

# 2. 重试装饰器
# Knowledge:
# - 根据参数控制重试次数和延迟
# - 支持指数退避
# - 处理不同类型的异常

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """重试装饰器工厂
    
    Args:
        max_attempts: 最大重试次数
        delay: 初始延迟时间（秒）
        backoff: 延迟时间的倍数
        exceptions: 需要重试的异常类型
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"尝试 {attempt + 1} 失败: {e}")
                        print(f"等待 {current_delay} 秒后重试...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print(f"所有 {max_attempts} 次尝试都失败了")
            
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ValueError,))
def unreliable_function():
    """一个不可靠的函数"""
    if random.random() < 0.8:  # 80% 概率失败
        raise ValueError("随机失败")
    return "成功!"

def demo_retry_decorator():
    print("\n=== 重试装饰器演示 ===")
    
    try:
        result = unreliable_function()
        print(f"最终结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")

# 3. 缓存装饰器
# Knowledge:
# - 根据参数控制缓存大小
# - 支持TTL（生存时间）
# - 内存管理

def cache(max_size=128, ttl=None):
    """缓存装饰器工厂
    
    Args:
        max_size: 缓存最大条目数
        ttl: 缓存生存时间（秒），None表示永不过期
    """
    def decorator(func):
        cache_dict = {}
        cache_times = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = str((args, sorted(kwargs.items())))
            
            # 检查TTL
            if ttl is not None:
                current_time = time.time()
                if key in cache_times:
                    if current_time - cache_times[key] > ttl:
                        del cache_dict[key]
                        del cache_times[key]
            
            # 检查缓存
            if key in cache_dict:
                print(f"缓存命中: {func.__name__}")
                return cache_dict[key]
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存储到缓存
            if len(cache_dict) >= max_size:
                # 简单的LRU：删除第一个条目
                oldest_key = next(iter(cache_dict))
                del cache_dict[oldest_key]
                if ttl is not None:
                    del cache_times[oldest_key]
            
            cache_dict[key] = result
            if ttl is not None:
                cache_times[key] = time.time()
            
            print(f"缓存存储: {func.__name__}")
            return result
        return wrapper
    return decorator

@cache(max_size=5, ttl=10)
def expensive_function(n):
    """模拟昂贵的计算"""
    print(f"执行昂贵计算: {n}")
    time.sleep(0.1)
    return n * n

def demo_cache_decorator():
    print("\n=== 缓存装饰器演示 ===")
    
    # 第一次调用
    result1 = expensive_function(5)
    print(f"结果: {result1}")
    
    # 第二次调用（应该从缓存获取）
    result2 = expensive_function(5)
    print(f"结果: {result2}")
    
    # 不同的参数
    result3 = expensive_function(10)
    print(f"结果: {result3}")

# 4. 权限检查装饰器
# Knowledge:
# - 根据用户角色进行权限控制
# - 支持多种权限级别
# - 灵活的权限配置

def require_permission(permission):
    """权限检查装饰器工厂"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 模拟用户权限检查
            user_permissions = getattr(wrapper, 'user_permissions', ['read'])
            
            if permission in user_permissions:
                return func(*args, **kwargs)
            else:
                raise PermissionError(f"需要权限: {permission}")
        return wrapper
    return decorator

@require_permission('admin')
def admin_only_function():
    return "管理员功能"

@require_permission('write')
def write_function():
    return "写入功能"

def demo_permission_decorator():
    print("\n=== 权限装饰器演示 ===")
    
    # 设置用户权限
    write_function.user_permissions = ['read', 'write']
    admin_only_function.user_permissions = ['read', 'write']  # 没有admin权限
    
    try:
        result = write_function()
        print(f"写入功能: {result}")
    except PermissionError as e:
        print(f"权限错误: {e}")
    
    try:
        result = admin_only_function()
        print(f"管理员功能: {result}")
    except PermissionError as e:
        print(f"权限错误: {e}")

# 5. 性能监控装饰器
# Knowledge:
# - 根据阈值进行性能监控
# - 支持不同的监控指标
# - 可配置的警告和错误级别

def performance_monitor(threshold=1.0, metric='time'):
    """性能监控装饰器工厂"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = get_memory_usage()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = get_memory_usage()
            
            execution_time = end_time - start_time
            memory_used = end_memory - start_memory
            
            if metric == 'time' and execution_time > threshold:
                print(f"⚠️  性能警告: {func.__name__} 执行时间 {execution_time:.3f}s 超过阈值 {threshold}s")
            elif metric == 'memory' and memory_used > threshold:
                print(f"⚠️  内存警告: {func.__name__} 内存使用 {memory_used:.2f}MB 超过阈值 {threshold}MB")
            
            return result
        return wrapper
    return decorator

def get_memory_usage():
    """获取当前内存使用（简化版）"""
    import os
    return os.getpid()  # 简化实现

@performance_monitor(threshold=0.5, metric='time')
def slow_function():
    time.sleep(0.6)
    return "慢函数完成"

def demo_performance_monitor():
    print("\n=== 性能监控装饰器演示 ===")
    
    result = slow_function()
    print(f"结果: {result}")

# 6. 验证装饰器
# Knowledge:
# - 根据规则验证输入参数
# - 支持自定义验证函数
# - 类型检查和范围验证

def validate_input(validation_rules):
    """输入验证装饰器工厂"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取函数参数
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # 验证参数
            for param_name, rules in validation_rules.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    
                    for rule in rules:
                        if not rule(value):
                            raise ValueError(f"参数 {param_name} 验证失败")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 验证规则
def is_positive(x):
    return x > 0

def is_string(x):
    return isinstance(x, str)

def is_between(min_val, max_val):
    def validator(x):
        return min_val <= x <= max_val
    return validator

@validate_input({
    'age': [is_positive, is_between(0, 150)],
    'name': [is_string]
})
def create_user(name, age):
    return f"用户 {name}, 年龄 {age}"

def demo_validation_decorator():
    print("\n=== 验证装饰器演示 ===")
    
    try:
        result = create_user("Alice", 25)
        print(f"结果: {result}")
    except ValueError as e:
        print(f"验证错误: {e}")
    
    try:
        result = create_user("Bob", -5)
        print(f"结果: {result}")
    except ValueError as e:
        print(f"验证错误: {e}")

# 7. 装饰器组合
# Knowledge:
# - 多个装饰器可以组合使用
# - 执行顺序：从下到上
# - 参数传递和返回值处理

@retry(max_attempts=2, delay=0.1)
@cache(max_size=10)
@performance_monitor(threshold=0.1)
def complex_function(n):
    """组合了多个装饰器的函数"""
    time.sleep(0.2)
    return f"复杂计算: {n * 2}"

def demo_decorator_composition():
    print("\n=== 装饰器组合演示 ===")
    
    # 第一次调用
    result1 = complex_function(5)
    print(f"第一次结果: {result1}")
    
    # 第二次调用（应该从缓存获取）
    result2 = complex_function(5)
    print(f"第二次结果: {result2}")

# 主函数
def main():
    print("🏭 带参数的装饰器工厂演示")
    print("=" * 50)
    
    demo_decorator_factory()
    demo_retry_decorator()
    demo_cache_decorator()
    demo_permission_decorator()
    demo_performance_monitor()
    demo_validation_decorator()
    demo_decorator_composition()
    
    print("\n✅ 参数化装饰器演示完成")

if __name__ == "__main__":
    main() 