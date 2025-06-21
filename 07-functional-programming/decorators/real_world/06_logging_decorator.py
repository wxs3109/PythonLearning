# ============================================================
# 📘 生产环境常见的日志装饰器
# ============================================================

import functools
import logging
import time
import traceback
import json
from datetime import datetime
from typing import Any, Callable, Dict, Optional

# 1. 基础日志装饰器
# Knowledge:
# - 使用 Python 标准库 logging
# - 记录函数调用和返回值
# - 配置日志级别和格式

def basic_logging_decorator(func: Callable) -> Callable:
    """基础日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        
        # 记录函数调用
        logger.info(f"调用函数: {func.__name__}")
        logger.debug(f"参数: args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"函数 {func.__name__} 执行成功")
            logger.debug(f"返回值: {result}")
            return result
        except Exception as e:
            logger.error(f"函数 {func.__name__} 执行失败: {e}")
            raise
    
    return wrapper

@basic_logging_decorator
def simple_function(x: int) -> int:
    """简单函数"""
    return x * 2

def demo_basic_logging():
    print("=== 基础日志装饰器演示 ===")
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    result = simple_function(5)
    print(f"结果: {result}")

# 2. 结构化日志装饰器
# Knowledge:
# - JSON 格式的日志输出
# - 结构化数据便于分析
# - 包含上下文信息

def structured_logging_decorator(func: Callable) -> Callable:
    """结构化日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        
        # 创建日志上下文
        log_context = {
            "function_name": func.__name__,
            "module": func.__module__,
            "timestamp": datetime.now().isoformat(),
            "args": str(args),
            "kwargs": str(kwargs)
        }
        
        # 记录函数调用
        logger.info("函数调用", extra={"context": log_context})
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # 记录成功信息
            log_context.update({
                "status": "success",
                "execution_time": execution_time,
                "result": str(result)
            })
            logger.info("函数执行成功", extra={"context": log_context})
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            
            # 记录错误信息
            log_context.update({
                "status": "error",
                "execution_time": execution_time,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            logger.error("函数执行失败", extra={"context": log_context})
            raise
    
    return wrapper

@structured_logging_decorator
def business_logic(user_id: int, action: str) -> Dict[str, Any]:
    """业务逻辑函数"""
    if user_id < 0:
        raise ValueError("用户ID不能为负数")
    
    return {
        "user_id": user_id,
        "action": action,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }

def demo_structured_logging():
    print("\n=== 结构化日志装饰器演示 ===")
    
    # 配置JSON格式日志
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName
            }
            
            if hasattr(record, 'context'):
                log_entry.update(record.context)
            
            return json.dumps(log_entry, ensure_ascii=False)
    
    # 设置日志处理器
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # 测试正常调用
    try:
        result = business_logic(123, "login")
        print(f"结果: {result}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 测试异常调用
    try:
        result = business_logic(-1, "login")
        print(f"结果: {result}")
    except Exception as e:
        print(f"异常: {e}")

# 3. 性能日志装饰器
# Knowledge:
# - 记录函数执行时间
# - 性能监控和告警
# - 慢查询识别

def performance_logging_decorator(threshold: float = 1.0) -> Callable:
    """性能日志装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            
            start_time = time.time()
            start_memory = get_memory_usage()
            
            try:
                result = func(*args, **kwargs)
                
                end_time = time.time()
                end_memory = get_memory_usage()
                
                execution_time = end_time - start_time
                memory_used = end_memory - start_memory
                
                # 记录性能信息
                performance_info = {
                    "function": func.__name__,
                    "execution_time": execution_time,
                    "memory_used": memory_used,
                    "args_count": len(args),
                    "kwargs_count": len(kwargs)
                }
                
                if execution_time > threshold:
                    logger.warning("函数执行时间超过阈值", extra={"performance": performance_info})
                else:
                    logger.info("函数执行完成", extra={"performance": performance_info})
                
                return result
            except Exception as e:
                end_time = time.time()
                execution_time = end_time - start_time
                
                logger.error(f"函数执行异常: {e}", extra={
                    "performance": {
                        "function": func.__name__,
                        "execution_time": execution_time,
                        "error": str(e)
                    }
                })
                raise
        
        return wrapper
    return decorator

def get_memory_usage() -> int:
    """获取当前内存使用（简化版）"""
    import os
    import psutil
    try:
        process = psutil.Process(os.getpid())
        return process.memory_info().rss // 1024  # KB
    except ImportError:
        return 0

@performance_logging_decorator(threshold=0.5)
def expensive_operation(n: int) -> int:
    """昂贵的操作"""
    time.sleep(0.6)  # 模拟耗时操作
    return sum(i * i for i in range(n))

def demo_performance_logging():
    print("\n=== 性能日志装饰器演示 ===")
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 测试性能监控
    result = expensive_operation(1000)
    print(f"结果: {result}")

# 4. 审计日志装饰器
# Knowledge:
# - 记录敏感操作
# - 用户行为追踪
# - 合规性要求

def audit_logging_decorator(sensitive_operations: list = None) -> Callable:
    """审计日志装饰器"""
    if sensitive_operations is None:
        sensitive_operations = ['delete', 'update', 'admin', 'payment']
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger('audit')
            
            # 检查是否为敏感操作
            is_sensitive = any(op in func.__name__.lower() for op in sensitive_operations)
            
            if is_sensitive:
                # 记录审计信息
                audit_info = {
                    "operation": func.__name__,
                    "user_id": get_current_user_id(),
                    "ip_address": get_client_ip(),
                    "timestamp": datetime.now().isoformat(),
                    "args": str(args),
                    "kwargs": str(kwargs)
                }
                
                logger.warning("敏感操作审计", extra={"audit": audit_info})
            
            try:
                result = func(*args, **kwargs)
                
                if is_sensitive:
                    audit_info["status"] = "success"
                    audit_info["result"] = str(result)
                    logger.info("敏感操作完成", extra={"audit": audit_info})
                
                return result
            except Exception as e:
                if is_sensitive:
                    audit_info["status"] = "failed"
                    audit_info["error"] = str(e)
                    logger.error("敏感操作失败", extra={"audit": audit_info})
                raise
        
        return wrapper
    return decorator

def get_current_user_id() -> Optional[int]:
    """获取当前用户ID（模拟）"""
    return 123

def get_client_ip() -> str:
    """获取客户端IP（模拟）"""
    return "192.168.1.100"

@audit_logging_decorator()
def delete_user(user_id: int) -> bool:
    """删除用户（敏感操作）"""
    print(f"删除用户: {user_id}")
    return True

@audit_logging_decorator()
def update_user_profile(user_id: int, data: dict) -> bool:
    """更新用户资料（敏感操作）"""
    print(f"更新用户 {user_id} 的资料: {data}")
    return True

def demo_audit_logging():
    print("\n=== 审计日志装饰器演示 ===")
    
    # 配置审计日志
    audit_logger = logging.getLogger('audit')
    audit_logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    audit_logger.addHandler(handler)
    
    # 测试敏感操作
    delete_user(456)
    update_user_profile(789, {"name": "John", "email": "john@example.com"})

# 5. 分布式追踪日志装饰器
# Knowledge:
# - 分布式系统中的请求追踪
# - 链路追踪和调试
# - 性能分析

def distributed_tracing_decorator(func: Callable) -> Callable:
    """分布式追踪日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('tracing')
        
        # 生成追踪ID
        trace_id = generate_trace_id()
        span_id = generate_span_id()
        
        # 记录追踪开始
        trace_info = {
            "trace_id": trace_id,
            "span_id": span_id,
            "operation": func.__name__,
            "start_time": datetime.now().isoformat(),
            "parent_span": get_parent_span_id()
        }
        
        logger.info("追踪开始", extra={"trace": trace_info})
        
        try:
            result = func(*args, **kwargs)
            
            # 记录追踪成功
            trace_info.update({
                "end_time": datetime.now().isoformat(),
                "status": "success",
                "result": str(result)
            })
            logger.info("追踪完成", extra={"trace": trace_info})
            
            return result
        except Exception as e:
            # 记录追踪失败
            trace_info.update({
                "end_time": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            })
            logger.error("追踪失败", extra={"trace": trace_info})
            raise
    
    return wrapper

def generate_trace_id() -> str:
    """生成追踪ID"""
    import uuid
    return str(uuid.uuid4())

def generate_span_id() -> str:
    """生成跨度ID"""
    import uuid
    return str(uuid.uuid4())[:8]

def get_parent_span_id() -> Optional[str]:
    """获取父跨度ID（模拟）"""
    return None

@distributed_tracing_decorator
def microservice_call(service_name: str, data: dict) -> dict:
    """微服务调用"""
    print(f"调用微服务: {service_name}")
    time.sleep(0.1)
    return {"service": service_name, "result": "success", "data": data}

def demo_distributed_tracing():
    print("\n=== 分布式追踪日志演示 ===")
    
    # 配置追踪日志
    tracing_logger = logging.getLogger('tracing')
    tracing_logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    tracing_logger.addHandler(handler)
    
    # 测试微服务调用
    result = microservice_call("user-service", {"user_id": 123})
    print(f"结果: {result}")

# 6. 生产环境最佳实践
# Knowledge:
# - 日志轮转和归档
# - 日志级别管理
# - 性能优化

def production_logging_decorator(
    level: str = "INFO",
    include_args: bool = True,
    include_result: bool = False,
    sensitive_fields: list = None
) -> Callable:
    """生产环境日志装饰器"""
    if sensitive_fields is None:
        sensitive_fields = ['password', 'token', 'secret']
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            
            # 过滤敏感信息
            safe_kwargs = kwargs.copy()
            for field in sensitive_fields:
                if field in safe_kwargs:
                    safe_kwargs[field] = "***"
            
            # 记录函数调用
            log_data = {
                "function": func.__name__,
                "module": func.__module__,
                "timestamp": datetime.now().isoformat()
            }
            
            if include_args:
                log_data["args"] = str(args)
                log_data["kwargs"] = str(safe_kwargs)
            
            logger.log(getattr(logging, level.upper()), 
                      f"函数调用: {func.__name__}", 
                      extra={"log_data": log_data})
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                log_data["execution_time"] = execution_time
                log_data["status"] = "success"
                
                if include_result:
                    log_data["result"] = str(result)
                
                logger.log(getattr(logging, level.upper()), 
                          f"函数完成: {func.__name__}", 
                          extra={"log_data": log_data})
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                
                log_data["execution_time"] = execution_time
                log_data["status"] = "error"
                log_data["error"] = str(e)
                
                logger.error(f"函数异常: {func.__name__}", 
                           extra={"log_data": log_data})
                raise
        
        return wrapper
    return decorator

@production_logging_decorator(
    level="INFO",
    include_args=True,
    include_result=False,
    sensitive_fields=['password', 'token']
)
def authenticate_user(username: str, password: str) -> dict:
    """用户认证"""
    print(f"认证用户: {username}")
    return {"user_id": 123, "username": username, "status": "authenticated"}

def demo_production_logging():
    print("\n=== 生产环境日志演示 ===")
    
    # 配置生产环境日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 测试认证
    result = authenticate_user("alice", "secret123")
    print(f"认证结果: {result}")

# 主函数
def main():
    print("📋 生产环境日志装饰器演示")
    print("=" * 50)
    
    demo_basic_logging()
    demo_structured_logging()
    demo_performance_logging()
    demo_audit_logging()
    demo_distributed_tracing()
    demo_production_logging()
    
    print("\n✅ 日志装饰器演示完成")

if __name__ == "__main__":
    main() 