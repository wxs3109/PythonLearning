# ============================================================
# 📘 类装饰器：__call__ / __init__ 实现
# ============================================================

import functools
import time

# 1. 类装饰器的基本概念
# Knowledge:
# - 类装饰器是一个类，可以装饰函数或类
# - 通过 __init__ 和 __call__ 方法实现
# - 可以维护状态和配置

class BasicClassDecorator:
    """基础类装饰器"""
    
    def __init__(self, func):
        """初始化时接收被装饰的函数"""
        self.func = func
        self.call_count = 0
        # 复制原函数的元数据
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        """调用时执行装饰逻辑"""
        self.call_count += 1
        print(f"🔢 第 {self.call_count} 次调用 {self.func.__name__}")
        result = self.func(*args, **kwargs)
        return result

@BasicClassDecorator
def simple_function():
    print("简单函数执行")
    return "简单结果"

def demo_basic_class_decorator():
    print("=== 基础类装饰器演示 ===")
    
    # 多次调用
    for i in range(3):
        result = simple_function()
        print(f"结果: {result}")
        print()

# 2. 带参数的类装饰器
# Knowledge:
# - 通过 __init__ 接收装饰器参数
# - 通过 __call__ 接收被装饰的函数
# - 支持复杂的配置选项

class ParameterizedClassDecorator:
    """带参数的类装饰器"""
    
    def __init__(self, prefix="[INFO]", max_calls=None):
        """初始化装饰器参数"""
        self.prefix = prefix
        self.max_calls = max_calls
        self.call_count = 0
    
    def __call__(self, func):
        """接收被装饰的函数"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.call_count += 1
            
            # 检查调用次数限制
            if self.max_calls and self.call_count > self.max_calls:
                raise RuntimeError(f"函数 {func.__name__} 调用次数超过限制 {self.max_calls}")
            
            print(f"{self.prefix} 调用 {func.__name__} (第 {self.call_count} 次)")
            result = func(*args, **kwargs)
            print(f"{self.prefix} {func.__name__} 完成")
            return result
        
        return wrapper

@ParameterizedClassDecorator(prefix="[DEBUG]", max_calls=3)
def debug_function():
    print("调试函数执行")
    return "调试结果"

@ParameterizedClassDecorator(prefix="[ERROR]")
def error_function():
    print("错误函数执行")
    return "错误结果"

def demo_parameterized_class_decorator():
    print("\n=== 带参数的类装饰器演示 ===")
    
    # 测试调用次数限制
    for i in range(4):
        try:
            result = debug_function()
            print(f"结果: {result}")
        except RuntimeError as e:
            print(f"错误: {e}")
            break
    
    print()
    
    # 测试无限制调用
    for i in range(2):
        result = error_function()
        print(f"结果: {result}")

# 3. 类装饰器装饰类
# Knowledge:
# - 类装饰器可以装饰类
# - 修改类的属性和方法
# - 添加新的功能

class ClassModifier:
    """修改类的装饰器"""
    
    def __init__(self, **kwargs):
        """初始化修改参数"""
        self.modifications = kwargs
    
    def __call__(self, cls):
        """接收被装饰的类"""
        # 添加新属性
        for name, value in self.modifications.items():
            setattr(cls, name, value)
        
        # 添加新方法
        def get_info(self):
            return f"类名: {cls.__name__}, 修改: {list(self.modifications.keys())}"
        
        cls.get_info = get_info
        
        # 修改现有方法
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            print(f"🔧 创建 {cls.__name__} 实例")
            original_init(self, *args, **kwargs)
        
        cls.__init__ = new_init
        
        return cls

@ClassModifier(version="1.0", author="Python")
class SimpleClass:
    """简单类"""
    
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"

def demo_class_modification():
    print("\n=== 类修改装饰器演示 ===")
    
    obj = SimpleClass("Alice")
    print(f"问候: {obj.greet()}")
    print(f"信息: {obj.get_info()}")
    print(f"版本: {obj.version}")
    print(f"作者: {obj.author}")

# 4. 单例模式类装饰器
# Knowledge:
# - 实现单例模式
# - 控制实例创建
# - 状态管理

class Singleton:
    """单例模式装饰器"""
    
    def __init__(self, cls):
        """初始化时接收类"""
        self.cls = cls
        self.instance = None
    
    def __call__(self, *args, **kwargs):
        """控制实例创建"""
        if self.instance is None:
            print(f"🆕 创建 {self.cls.__name__} 的唯一实例")
            self.instance = self.cls(*args, **kwargs)
        else:
            print(f"♻️  返回 {self.cls.__name__} 的现有实例")
        return self.instance

@Singleton
class DatabaseConnection:
    """数据库连接类"""
    
    def __init__(self, host="localhost"):
        self.host = host
        self.connected = False
    
    def connect(self):
        if not self.connected:
            print(f"连接到数据库: {self.host}")
            self.connected = True
        return self.connected
    
    def query(self, sql):
        if self.connected:
            return f"执行查询: {sql}"
        else:
            raise RuntimeError("数据库未连接")

def demo_singleton_decorator():
    print("\n=== 单例装饰器演示 ===")
    
    # 创建多个实例（实际是同一个）
    db1 = DatabaseConnection("server1")
    db2 = DatabaseConnection("server2")
    
    print(f"db1 是 db2: {db1 is db2}")
    print(f"db1.host: {db1.host}")
    print(f"db2.host: {db2.host}")
    
    # 测试连接
    db1.connect()
    print(db1.query("SELECT * FROM users"))

# 5. 缓存类装饰器
# Knowledge:
# - 实现方法缓存
# - 缓存策略管理
# - 内存优化

class MethodCache:
    """方法缓存装饰器"""
    
    def __init__(self, max_size=100, ttl=None):
        """初始化缓存参数"""
        self.max_size = max_size
        self.ttl = ttl
        self.cache = {}
        self.timestamps = {}
    
    def __call__(self, cls):
        """装饰类"""
        # 为每个方法添加缓存
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not attr_name.startswith('_'):
                # 创建缓存方法
                cached_method = self._create_cached_method(attr)
                setattr(cls, attr_name, cached_method)
        
        return cls
    
    def _create_cached_method(self, method):
        """创建缓存方法"""
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            # 创建缓存键
            key = f"{method.__name__}:{str((args, sorted(kwargs.items())))}"
            
            # 检查TTL
            if self.ttl is not None:
                current_time = time.time()
                if key in self.timestamps:
                    if current_time - self.timestamps[key] > self.ttl:
                        del self.cache[key]
                        del self.timestamps[key]
            
            # 检查缓存
            if key in self.cache:
                print(f"💾 缓存命中: {method.__name__}")
                return self.cache[key]
            
            # 执行方法
            result = method(self, *args, **kwargs)
            
            # 存储到缓存
            if len(self.cache) >= self.max_size:
                # 简单的LRU：删除第一个条目
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                if self.ttl is not None:
                    del self.timestamps[oldest_key]
            
            self.cache[key] = result
            if self.ttl is not None:
                self.timestamps[key] = time.time()
            
            print(f"💾 缓存存储: {method.__name__}")
            return result
        
        return wrapper

@MethodCache(max_size=10, ttl=5)
class Calculator:
    """计算器类"""
    
    def __init__(self):
        self.operation_count = 0
    
    def expensive_calculation(self, n):
        """昂贵的计算"""
        self.operation_count += 1
        print(f"执行昂贵计算: {n}")
        time.sleep(0.1)  # 模拟计算时间
        return n * n
    
    def fibonacci(self, n):
        """斐波那契数列"""
        self.operation_count += 1
        print(f"计算斐波那契: {n}")
        if n <= 1:
            return n
        return self.fibonacci(n-1) + self.fibonacci(n-2)

def demo_method_cache():
    print("\n=== 方法缓存装饰器演示 ===")
    
    calc = Calculator()
    
    # 第一次调用
    result1 = calc.expensive_calculation(5)
    print(f"结果: {result1}")
    
    # 第二次调用（应该从缓存获取）
    result2 = calc.expensive_calculation(5)
    print(f"结果: {result2}")
    
    # 不同的参数
    result3 = calc.expensive_calculation(10)
    print(f"结果: {result3}")
    
    print(f"操作次数: {calc.operation_count}")

# 6. 性能监控类装饰器
# Knowledge:
# - 监控类方法的性能
# - 收集统计信息
# - 性能分析

class PerformanceMonitor:
    """性能监控装饰器"""
    
    def __init__(self, threshold=1.0):
        """初始化监控参数"""
        self.threshold = threshold
        self.stats = {}
    
    def __call__(self, cls):
        """装饰类"""
        # 为每个方法添加性能监控
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not attr_name.startswith('_'):
                monitored_method = self._create_monitored_method(attr)
                setattr(cls, attr_name, monitored_method)
        
        # 添加统计方法
        def get_stats(self):
            return self.stats
        
        cls.get_stats = get_stats
        
        return cls
    
    def _create_monitored_method(self, method):
        """创建监控方法"""
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            
            result = method(self, *args, **kwargs)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # 更新统计信息
            if method.__name__ not in self.stats:
                self.stats[method.__name__] = {
                    'calls': 0,
                    'total_time': 0,
                    'avg_time': 0,
                    'max_time': 0
                }
            
            stats = self.stats[method.__name__]
            stats['calls'] += 1
            stats['total_time'] += execution_time
            stats['avg_time'] = stats['total_time'] / stats['calls']
            stats['max_time'] = max(stats['max_time'], execution_time)
            
            # 检查性能阈值
            if execution_time > self.threshold:
                print(f"⚠️  性能警告: {method.__name__} 执行时间 {execution_time:.3f}s 超过阈值 {self.threshold}s")
            
            return result
        
        return wrapper

@PerformanceMonitor(threshold=0.5)
class DataProcessor:
    """数据处理类"""
    
    def __init__(self):
        self.data = []
    
    def process_data(self, items):
        """处理数据"""
        time.sleep(0.6)  # 模拟处理时间
        self.data.extend(items)
        return len(self.data)
    
    def analyze_data(self):
        """分析数据"""
        time.sleep(0.2)
        return f"分析了 {len(self.data)} 个数据项"

def demo_performance_monitor():
    print("\n=== 性能监控装饰器演示 ===")
    
    processor = DataProcessor()
    
    # 执行操作
    processor.process_data([1, 2, 3])
    processor.analyze_data()
    processor.process_data([4, 5, 6])
    
    # 查看统计信息
    stats = processor.get_stats()
    for method, stat in stats.items():
        print(f"{method}:")
        print(f"  调用次数: {stat['calls']}")
        print(f"  总时间: {stat['total_time']:.3f}s")
        print(f"  平均时间: {stat['avg_time']:.3f}s")
        print(f"  最大时间: {stat['max_time']:.3f}s")

# 7. 类装饰器的最佳实践
# Knowledge:
# - 设计原则
# - 性能考虑
# - 调试技巧

class BestPracticeDecorator:
    """最佳实践类装饰器"""
    
    def __init__(self, **options):
        """初始化选项"""
        self.options = options
        self._setup()
    
    def _setup(self):
        """设置装饰器"""
        # 验证选项
        if 'max_calls' in self.options:
            if self.options['max_calls'] <= 0:
                raise ValueError("max_calls 必须大于 0")
    
    def __call__(self, target):
        """装饰目标"""
        if callable(target):
            return self._decorate_function(target)
        else:
            raise TypeError("只能装饰可调用对象")
    
    def _decorate_function(self, func):
        """装饰函数"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 前置处理
            self._pre_process(func, *args, **kwargs)
            
            try:
                result = func(*args, **kwargs)
                # 后置处理
                self._post_process(func, result)
                return result
            except Exception as e:
                # 异常处理
                self._handle_exception(func, e)
                raise
        
        return wrapper
    
    def _pre_process(self, func, *args, **kwargs):
        """前置处理"""
        print(f"🔧 前置处理: {func.__name__}")
    
    def _post_process(self, func, result):
        """后置处理"""
        print(f"🔧 后置处理: {func.__name__} -> {result}")
    
    def _handle_exception(self, func, exception):
        """异常处理"""
        print(f"❌ 异常处理: {func.__name__} -> {exception}")

@BestPracticeDecorator(max_calls=5)
def best_practice_function(x):
    """最佳实践函数"""
    if x < 0:
        raise ValueError("x 不能为负数")
    return x * 2

def demo_best_practices():
    print("\n=== 最佳实践演示 ===")
    
    # 正常调用
    try:
        result = best_practice_function(5)
        print(f"结果: {result}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 异常调用
    try:
        result = best_practice_function(-1)
        print(f"结果: {result}")
    except Exception as e:
        print(f"异常: {e}")

# 主函数
def main():
    print("🏗️  类装饰器演示")
    print("=" * 50)
    
    demo_basic_class_decorator()
    demo_parameterized_class_decorator()
    demo_class_modification()
    demo_singleton_decorator()
    demo_method_cache()
    demo_performance_monitor()
    demo_best_practices()
    
    print("\n✅ 类装饰器演示完成")

if __name__ == "__main__":
    main() 