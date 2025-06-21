# ============================================================
# 📘 functools.wraps 的作用与正确用法
# ============================================================

import functools
import inspect

# 1. 问题：装饰器丢失元数据
# Knowledge:
# - 装饰器会改变原函数的元数据
# - __name__, __doc__, __module__, __annotations__ 等会丢失
# - 这会影响调试、文档生成和反射

def bad_decorator(func):
    """不好的装饰器：丢失元数据"""
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def example_function(a: int, b: str = "default") -> str:
    """这是一个示例函数，有类型注解和文档字符串"""
    return f"{a} - {b}"

def demo_metadata_loss():
    print("=== 元数据丢失问题 ===")
    
    print("原始函数的元数据:")
    print(f"  __name__: {example_function.__name__}")
    print(f"  __doc__: {example_function.__doc__}")
    print(f"  __module__: {example_function.__module__}")
    print(f"  __annotations__: {example_function.__annotations__}")
    print(f"  __defaults__: {example_function.__defaults__}")
    print(f"  __qualname__: {example_function.__qualname__}")

# 2. 解决方案：使用 functools.wraps
# Knowledge:
# - functools.wraps 是一个装饰器
# - 它复制原函数的元数据到包装函数
# - 这是装饰器的最佳实践

def good_decorator(func):
    """好的装饰器：保留元数据"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def example_function_good(a: int, b: str = "default") -> str:
    """这是一个示例函数，有类型注解和文档字符串"""
    return f"{a} - {b}"

def demo_metadata_preservation():
    print("\n=== 元数据保留解决方案 ===")
    
    print("使用 functools.wraps 后的元数据:")
    print(f"  __name__: {example_function_good.__name__}")
    print(f"  __doc__: {example_function_good.__doc__}")
    print(f"  __module__: {example_function_good.__module__}")
    print(f"  __annotations__: {example_function_good.__annotations__}")
    print(f"  __defaults__: {example_function_good.__defaults__}")
    print(f"  __qualname__: {example_function_good.__qualname__}")

# 3. functools.wraps 的详细用法
# Knowledge:
# - wraps 可以指定要复制的属性
# - 可以自定义要保留的元数据
# - 支持部分属性复制

def custom_wraps_decorator(func):
    """自定义 wraps 装饰器"""
    @functools.wraps(func, assigned=('__name__', '__doc__', '__annotations__'))
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@custom_wraps_decorator
def custom_function(a: int) -> str:
    """自定义函数"""
    return str(a)

def demo_custom_wraps():
    print("\n=== 自定义 wraps 用法 ===")
    
    print("自定义 wraps 的结果:")
    print(f"  __name__: {custom_function.__name__}")
    print(f"  __doc__: {custom_function.__doc__}")
    print(f"  __annotations__: {custom_function.__annotations__}")
    print(f"  __module__: {custom_function.__module__}")  # 可能不会保留

# 4. 实际应用场景
# Knowledge:
# - 调试和日志记录
# - 文档生成工具
# - 测试框架
# - IDE 智能提示

def logging_decorator(func):
    """生产环境日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 使用正确的函数名进行日志记录
        print(f"[LOG] 调用函数: {func.__name__}")
        print(f"[LOG] 函数文档: {func.__doc__}")
        print(f"[LOG] 函数签名: {inspect.signature(func)}")
        
        result = func(*args, **kwargs)
        print(f"[LOG] 函数 {func.__name__} 执行完成")
        return result
    return wrapper

@logging_decorator
def business_logic(user_id: int, action: str) -> bool:
    """业务逻辑函数
    
    Args:
        user_id: 用户ID
        action: 执行的操作
        
    Returns:
        操作是否成功
    """
    print(f"执行业务逻辑: 用户 {user_id} 执行 {action}")
    return True

def demo_real_world_usage():
    print("\n=== 实际应用场景 ===")
    
    result = business_logic(123, "login")
    print(f"结果: {result}")

# 5. 调试和检查元数据
# Knowledge:
# - 使用 inspect 模块检查函数信息
# - 验证装饰器是否正确保留了元数据
# - 调试装饰器问题

def inspect_function_metadata(func):
    """检查函数元数据的工具函数"""
    print(f"函数名: {func.__name__}")
    print(f"文档字符串: {func.__doc__}")
    print(f"模块: {func.__module__}")
    print(f"类型注解: {func.__annotations__}")
    print(f"默认参数: {func.__defaults__}")
    print(f"限定名: {func.__qualname__}")
    print(f"签名: {inspect.signature(func)}")
    print(f"源代码: {inspect.getsource(func)}")

def demo_inspection():
    print("\n=== 函数元数据检查 ===")
    
    print("检查原始函数:")
    inspect_function_metadata(business_logic)

# 6. 常见错误和陷阱
# Knowledge:
# - 忘记使用 wraps 的后果
# - 部分属性丢失的问题
# - 调试时的困惑

def problematic_decorator(func):
    """有问题的装饰器"""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # 忘记使用 wraps
    return wrapper

@problematic_decorator
def test_function(a: int) -> str:
    """测试函数"""
    return str(a)

def demo_problems():
    print("\n=== 常见问题演示 ===")
    
    print("有问题的装饰器:")
    print(f"  __name__: {test_function.__name__}")
    print(f"  __doc__: {test_function.__doc__}")
    print(f"  __annotations__: {test_function.__annotations__}")
    
    # 这会导致调试困难
    print(f"  调试时看到的函数名: {test_function.__name__}")

# 7. 最佳实践
# Knowledge:
# - 总是使用 functools.wraps
# - 保持装饰器的简洁性
# - 考虑元数据的重要性

def best_practice_decorator(func):
    """最佳实践装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 装饰器逻辑
        print(f"装饰器: 调用 {func.__name__}")
        
        # 调用原函数
        result = func(*args, **kwargs)
        
        # 装饰器逻辑
        print(f"装饰器: {func.__name__} 完成")
        
        return result
    return wrapper

@best_practice_decorator
def best_practice_function(x: int, y: int = 0) -> int:
    """最佳实践函数示例"""
    return x + y

def demo_best_practices():
    print("\n=== 最佳实践演示 ===")
    
    print("最佳实践装饰器:")
    print(f"  __name__: {best_practice_function.__name__}")
    print(f"  __doc__: {best_practice_function.__doc__}")
    print(f"  __annotations__: {best_practice_function.__annotations__}")
    
    # 测试调用
    result = best_practice_function(5, 3)
    print(f"  调用结果: {result}")

# 主函数
def main():
    print("🔧 functools.wraps 演示")
    print("=" * 50)
    
    demo_metadata_loss()
    demo_metadata_preservation()
    demo_custom_wraps()
    demo_real_world_usage()
    demo_inspection()
    demo_problems()
    demo_best_practices()
    
    print("\n✅ wraps 演示完成")

if __name__ == "__main__":
    main() 