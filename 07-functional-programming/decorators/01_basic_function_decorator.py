# ============================================================
# 📘 基础函数装饰器：闭包 + @ 语法入门
# ============================================================

import time
import functools

# 1. 闭包基础回顾
# Knowledge:
# - 闭包是函数和其词法环境的组合
# - 内部函数可以访问外部函数的变量
# - 装饰器本质上就是闭包的应用

def outer_function(x):
    """外部函数"""
    def inner_function(y):
        """内部函数（闭包）"""
        return x + y  # 访问外部函数的变量 x
    return inner_function

def demo_closure():
    print("=== 闭包基础演示 ===")
    
    # 创建闭包
    add_five = outer_function(5)
    add_ten = outer_function(10)
    
    print(f"add_five(3) = {add_five(3)}")  # 8
    print(f"add_ten(3) = {add_ten(3)}")    # 13
    
    # 查看闭包信息
    print(f"add_five.__closure__: {add_five.__closure__}")
    print(f"add_five.__code__.co_freevars: {add_five.__code__.co_freevars}")

# 2. 最简单的装饰器
# Knowledge:
# - 装饰器是一个函数，接受一个函数作为参数
# - 返回一个新函数，通常包装了原函数
# - @ 语法是语法糖

def simple_decorator(func):
    """最简单的装饰器"""
    def wrapper():
        print(f"调用函数: {func.__name__}")
        result = func()
        print(f"函数 {func.__name__} 执行完成")
        return result
    return wrapper

@simple_decorator
def hello():
    print("Hello, World!")

def demo_simple_decorator():
    print("\n=== 简单装饰器演示 ===")
    
    # 使用 @ 语法
    hello()
    
    print("\n等价于:")
    # 手动调用装饰器
    decorated_hello = simple_decorator(hello)
    decorated_hello()

# 3. 带参数的函数装饰器
# Knowledge:
# - 装饰器需要处理任意参数
# - 使用 *args 和 **kwargs 传递参数
# - 保持原函数的签名

def log_function(func):
    """记录函数调用的装饰器"""
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"参数: args={args}, kwargs={kwargs}")
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.4f} 秒")
        print(f"返回值: {result}")
        return result
    return wrapper

@log_function
def add(a, b):
    """简单的加法函数"""
    time.sleep(0.1)  # 模拟计算时间
    return a + b

@log_function
def greet(name, greeting="Hello"):
    """问候函数"""
    time.sleep(0.05)
    return f"{greeting}, {name}!"

def demo_parameterized_decorator():
    print("\n=== 带参数的装饰器演示 ===")
    
    # 测试不同参数
    result1 = add(3, 5)
    result2 = greet("Alice", "Hi")
    result3 = greet("Bob")  # 使用默认参数

# 4. 装饰器的问题：元数据丢失
# Knowledge:
# - 装饰器会改变原函数的元数据
# - __name__, __doc__, __module__ 等会丢失
# - 需要使用 functools.wraps 保留元数据

def bad_decorator(func):
    """不好的装饰器：丢失元数据"""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def good_decorator(func):
    """好的装饰器：保留元数据"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def function_with_metadata():
    """这是一个有文档字符串的函数"""
    return "Hello"

@good_decorator
def function_with_metadata_good():
    """这是一个有文档字符串的函数"""
    return "Hello"

def demo_metadata_preservation():
    print("\n=== 元数据保留演示 ===")
    
    print("不好的装饰器:")
    print(f"  __name__: {function_with_metadata.__name__}")
    print(f"  __doc__: {function_with_metadata.__doc__}")
    
    print("\n好的装饰器:")
    print(f"  __name__: {function_with_metadata_good.__name__}")
    print(f"  __doc__: {function_with_metadata_good.__doc__}")

# 5. 装饰器的实际应用
# Knowledge:
# - 装饰器常用于横切关注点
# - 日志、性能监控、权限检查等
# - 代码复用和关注点分离

def retry(max_attempts=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"尝试 {attempt + 1} 失败，{delay} 秒后重试...")
                        time.sleep(delay)
            
            print(f"所有 {max_attempts} 次尝试都失败了")
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_function():
    """一个不可靠的函数，可能失败"""
    import random
    if random.random() < 0.7:  # 70% 概率失败
        raise ValueError("随机失败")
    return "成功!"

def demo_real_world_decorator():
    print("\n=== 实际应用装饰器演示 ===")
    
    try:
        result = unreliable_function()
        print(f"最终结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")

# 6. 装饰器的调试技巧
# Knowledge:
# - 使用 inspect 模块检查函数信息
# - 调试装饰器时的常见问题
# - 如何追踪装饰器调用

import inspect

def debug_decorator(func):
    """调试装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调试信息:")
        print(f"  函数名: {func.__name__}")
        print(f"  参数: {inspect.signature(func)}")
        print(f"  调用参数: args={args}, kwargs={kwargs}")
        
        result = func(*args, **kwargs)
        print(f"  返回值: {result}")
        return result
    return wrapper

@debug_decorator
def test_function(a, b, c=10):
    """测试函数"""
    return a + b + c

def demo_debug_decorator():
    print("\n=== 调试装饰器演示 ===")
    
    test_function(1, 2, c=5)
    test_function(10, 20)

# 主函数
def main():
    print("🎭 基础函数装饰器演示")
    print("=" * 50)
    
    demo_closure()
    demo_simple_decorator()
    demo_parameterized_decorator()
    demo_metadata_preservation()
    demo_real_world_decorator()
    demo_debug_decorator()
    
    print("\n✅ 基础装饰器演示完成")

if __name__ == "__main__":
    main() 