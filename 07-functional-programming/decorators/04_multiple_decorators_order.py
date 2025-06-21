# ============================================================
# 📘 多重装饰器叠加时的执行顺序
# ============================================================

import functools
import time

# 1. 装饰器执行顺序的基本概念
# Knowledge:
# - 装饰器从下到上执行（最接近函数的先执行）
# - 调用时从上到下执行（最外层的先执行）
# - 等价于：func = decorator1(decorator2(decorator3(func)))

def decorator1(func):
    """第一个装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("🔴 装饰器1: 进入")
        result = func(*args, **kwargs)
        print("🔴 装饰器1: 退出")
        return result
    return wrapper

def decorator2(func):
    """第二个装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("🟡 装饰器2: 进入")
        result = func(*args, **kwargs)
        print("🟡 装饰器2: 退出")
        return result
    return wrapper

def decorator3(func):
    """第三个装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("🟢 装饰器3: 进入")
        result = func(*args, **kwargs)
        print("🟢 装饰器3: 退出")
        return result
    return wrapper

@decorator1
@decorator2
@decorator3
def test_function():
    print("📝 原始函数执行")
    return "函数结果"

def demo_basic_order():
    print("=== 基本执行顺序演示 ===")
    print("装饰器顺序: @decorator1 @decorator2 @decorator3")
    print("等价于: decorator1(decorator2(decorator3(test_function)))")
    print()
    
    result = test_function()
    print(f"最终结果: {result}")

# 2. 装饰器执行顺序的详细分析
# Knowledge:
# - 装饰器应用顺序：从下到上
# - 函数调用顺序：从上到下
# - 每个装饰器都会包装前一个装饰器的结果

def timing_decorator(func):
    """计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️  {func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

def logging_decorator(func):
    """日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📋 调用函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"📋 函数 {func.__name__} 完成")
        return result
    return wrapper

def validation_decorator(func):
    """验证装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"✅ 验证函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"✅ 验证完成: {func.__name__}")
        return result
    return wrapper

@timing_decorator
@logging_decorator
@validation_decorator
def complex_function(n):
    """复杂函数"""
    print(f"🎯 执行业务逻辑: {n}")
    time.sleep(0.1)
    return n * 2

def demo_detailed_order():
    print("\n=== 详细执行顺序分析 ===")
    print("装饰器顺序: @timing @logging @validation")
    print("应用顺序: validation -> logging -> timing")
    print("调用顺序: timing -> logging -> validation -> function")
    print()
    
    result = complex_function(5)
    print(f"最终结果: {result}")

# 3. 装饰器链的等价形式
# Knowledge:
# - 多重装饰器等价于嵌套调用
# - 可以手动构建装饰器链
# - 理解装饰器的本质

def demo_equivalent_forms():
    print("\n=== 等价形式演示 ===")
    
    # 方式1：使用 @ 语法
    @decorator1
    @decorator2
    def function1():
        print("函数1执行")
        return "结果1"
    
    # 方式2：手动嵌套调用
    def function2():
        print("函数2执行")
        return "结果2"
    
    decorated_function2 = decorator1(decorator2(function2))
    
    print("方式1结果:")
    function1()
    print()
    
    print("方式2结果:")
    decorated_function2()

# 4. 装饰器参数传递
# Knowledge:
# - 装饰器之间的参数传递
# - 返回值处理
# - 异常传播

def param_logging_decorator(func):
    """参数日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📝 参数日志: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"📝 返回值: {result}")
        return result
    return wrapper

def error_handling_decorator(func):
    """错误处理装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"❌ 错误处理: {e}")
            raise
    return wrapper

@error_handling_decorator
@param_logging_decorator
def function_with_params(a, b, c=10):
    """带参数的函数"""
    if a < 0:
        raise ValueError("a 不能为负数")
    return a + b + c

def demo_parameter_passing():
    print("\n=== 参数传递演示 ===")
    
    # 正常调用
    try:
        result = function_with_params(1, 2, c=5)
        print(f"正常调用结果: {result}")
    except Exception as e:
        print(f"异常: {e}")
    
    print()
    
    # 异常调用
    try:
        result = function_with_params(-1, 2)
        print(f"异常调用结果: {result}")
    except Exception as e:
        print(f"异常: {e}")

# 5. 装饰器状态管理
# Knowledge:
# - 装饰器之间的状态共享
# - 闭包变量的作用域
# - 装饰器实例的生命周期

def state_decorator(name):
    """状态装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.call_count = getattr(wrapper, 'call_count', 0) + 1
            print(f"🔄 {name} 装饰器: 第 {wrapper.call_count} 次调用")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@state_decorator("外层")
@state_decorator("内层")
def stateful_function():
    print("状态函数执行")
    return "状态结果"

def demo_state_management():
    print("\n=== 状态管理演示 ===")
    
    # 多次调用
    for i in range(3):
        print(f"\n第 {i+1} 次调用:")
        result = stateful_function()
        print(f"结果: {result}")

# 6. 装饰器性能影响
# Knowledge:
# - 装饰器的性能开销
# - 多层装饰器的影响
# - 优化策略

def performance_decorator(func):
    """性能装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        wrapper.total_time = getattr(wrapper, 'total_time', 0) + (end_time - start_time)
        wrapper.call_count = getattr(wrapper, 'call_count', 0) + 1
        return result
    return wrapper

@performance_decorator
@performance_decorator
@performance_decorator
def performance_test_function():
    """性能测试函数"""
    time.sleep(0.01)
    return "性能测试"

def demo_performance_impact():
    print("\n=== 性能影响演示 ===")
    
    # 多次调用
    for i in range(5):
        result = performance_test_function()
    
    print(f"总调用次数: {performance_test_function.call_count}")
    print(f"总执行时间: {performance_test_function.total_time:.4f}秒")
    print(f"平均执行时间: {performance_test_function.total_time / performance_test_function.call_count:.4f}秒")

# 7. 装饰器调试技巧
# Knowledge:
# - 如何调试装饰器链
# - 装饰器执行追踪
# - 问题定位方法

def debug_decorator(func):
    """调试装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🐛 调试: 进入 {func.__name__}")
        print(f"🐛 调试: 参数 {args}, {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            print(f"🐛 调试: 正常返回 {result}")
            return result
        except Exception as e:
            print(f"🐛 调试: 异常 {e}")
            raise
        finally:
            print(f"🐛 调试: 退出 {func.__name__}")
    return wrapper

@debug_decorator
@debug_decorator
def debug_test_function(x):
    """调试测试函数"""
    if x < 0:
        raise ValueError("x 不能为负数")
    return x * 2

def demo_debugging():
    print("\n=== 调试技巧演示 ===")
    
    # 正常调用
    try:
        result = debug_test_function(5)
        print(f"调试结果: {result}")
    except Exception as e:
        print(f"调试异常: {e}")
    
    print()
    
    # 异常调用
    try:
        result = debug_test_function(-1)
        print(f"调试结果: {result}")
    except Exception as e:
        print(f"调试异常: {e}")

# 8. 最佳实践
# Knowledge:
# - 装饰器设计原则
# - 避免常见陷阱
# - 性能优化建议

def best_practice_decorator(func):
    """最佳实践装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. 总是使用 functools.wraps
        # 2. 正确处理参数和返回值
        # 3. 适当的错误处理
        # 4. 避免副作用
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # 记录错误但不隐藏
            print(f"⚠️  装饰器捕获异常: {e}")
            raise
    return wrapper

@best_practice_decorator
def best_practice_function():
    """最佳实践函数"""
    return "最佳实践"

def demo_best_practices():
    print("\n=== 最佳实践演示 ===")
    
    result = best_practice_function()
    print(f"结果: {result}")
    print(f"函数名: {best_practice_function.__name__}")
    print(f"文档: {best_practice_function.__doc__}")

# 主函数
def main():
    print("🔄 多重装饰器执行顺序演示")
    print("=" * 50)
    
    demo_basic_order()
    demo_detailed_order()
    demo_equivalent_forms()
    demo_parameter_passing()
    demo_state_management()
    demo_performance_impact()
    demo_debugging()
    demo_best_practices()
    
    print("\n✅ 多重装饰器演示完成")

if __name__ == "__main__":
    main() 