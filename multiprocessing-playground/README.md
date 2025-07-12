# Multiprocessing Playground

一个全面的 Python multiprocessing 学习项目，包含从基础到高级的所有概念和实践。

## 📁 项目结构

```
multiprocessing-playground/
├── README.md                         # 项目说明与导航
│
├── 0_basics/                         # 基础概念：进程 vs 线程
│   ├── process_vs_thread.py
│   ├── creating_process.py
│   ├── join_terminate.py
│   └── process_contexts.py           # spawn / fork / forkserver
│
├── 1_synchronization/                # 同步原语
│   ├── locks.py
│   ├── rlock.py
│   ├── semaphores.py
│   ├── events.py
│   ├── conditions.py
│   └── barrier.py
│
├── 2_communication/                  # 进程间通信
│   ├── queues_and_pipes/             # 队列和管道
│   │   ├── queues_basic.py
│   │   ├── pipes_basic.py
│   │   └── priority_queue_example.py
│   └── shared_memory/                # 内存共享
│       ├── shm_basics.py
│       ├── array_value_ctypes.py
│       ├── manager_dict_list.py
│       └── numpy_sharedmem.py
│
├── 3_pools/                          # Pool 用法专栏
│   ├── pool_map_apply.py
│   ├── imap_async.py
│   ├── chunksize_tuning.py
│   └── starmap_async.py
│
├── 4_patterns/                       # 典型并发模式
│   ├── producer_consumer.py
│   ├── worker_pool_pattern.py
│   ├── pipeline_fanout_fanin.py
│   └── mapreduce_example.py
│
├── 5_advanced/                       # 进阶/坑点
│   ├── daemon_process.py
│   ├── initializer_finalizer.py
│   ├── process_inheritance.py
│   ├── custom_context.py
│   └── error_handling_retry.py
│
├── 6_performance/                    # 性能与调优
│   ├── cpu_vs_io_bound.py
│   ├── profiling_mp_programs.py
│   ├── affinity_and_numa.py
│   └── memory_overhead_benchmark.py
│
├── 7_integration/                    # 与其他框架联动
│   ├── asyncio_bridge.py
│   ├── async_multiprocessing_pattern.py
│   ├── dask_comparison.py
│   └── ray_comparison.py
│
└── tests/                            # pytest 单元/负载测试
    ├── test_synchronization.py
    ├── test_shared_memory.py
    └── test_pool_throughput.py
```

## 🚀 学习路径

### 0. 基础概念 (0_basics/)
- **进程 vs 线程** - 理解基本区别
- **创建进程** - Process 类的使用
- **进程控制** - join, terminate, kill
- **进程上下文** - spawn, fork, forkserver

### 1. 同步原语 (1_synchronization/)
- **Lock** - 互斥锁
- **RLock** - 可重入锁
- **Semaphore** - 信号量
- **Event** - 事件
- **Condition** - 条件变量
- **Barrier** - 屏障

### 2. 进程间通信 (2_communication/)
- **队列和管道** - Queue, Pipe
- **共享内存** - SharedMemory, Array, Value
- **Manager** - 进程管理器

### 3. 进程池 (3_pools/)
- **map/apply** - 基本用法
- **imap/async** - 迭代器和异步
- **chunksize** - 性能调优
- **starmap** - 多参数映射

### 4. 并发模式 (4_patterns/)
- **生产者-消费者** - 经典模式
- **工作池** - 任务分发
- **管道模式** - 数据流处理
- **MapReduce** - 分布式计算

### 5. 进阶主题 (5_advanced/)
- **守护进程** - daemon 属性
- **初始化和清理** - initializer/finalizer
- **进程继承** - 资源传递
- **自定义上下文** - 进程环境
- **错误处理** - 异常和重试

### 6. 性能优化 (6_performance/)
- **CPU vs I/O 密集型** - 任务分类
- **性能分析** - 瓶颈识别
- **CPU 亲和性** - 硬件优化
- **内存开销** - 基准测试

### 7. 框架集成 (7_integration/)
- **asyncio 桥接** - 异步多进程
- **Dask 对比** - 分布式计算
- **Ray 对比** - 大规模并行

## 🛠️ 环境要求

```bash
# Python 3.7+
python --version

# 安装基本依赖 (推荐)
pip install -r requirements.txt

# 或者手动安装核心依赖
pip install numpy psutil pytest matplotlib

# 可选依赖 (取消注释 requirements.txt 中的相应部分)
# pip install dask ray
```

## 📖 使用方法

### 运行单个示例
```bash
cd multiprocessing-playground
python 0_basics/creating_process.py
```

### 运行测试
```bash
pytest tests/
```

### 性能基准测试
```bash
python 6_performance/memory_overhead_benchmark.py
```

## 🎯 关键概念

### 进程 vs 线程
- **进程**: 独立内存空间，适合 CPU 密集型
- **线程**: 共享内存空间，适合 I/O 密集型

### 进程间通信
- **Queue**: 线程安全的队列
- **Pipe**: 双向通信管道
- **SharedMemory**: 共享内存块

### 同步机制
- **Lock**: 互斥访问
- **Semaphore**: 限制并发数
- **Event**: 进程间通知

## ⚠️ 注意事项

1. **Windows 兼容性** - 使用 `spawn` 上下文
2. **内存开销** - 每个进程独立内存空间
3. **序列化限制** - 只能传递可序列化对象
4. **资源清理** - 及时关闭进程和连接

## 🔧 调试技巧

1. **启用日志**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **进程监控**
```python
import psutil
print(f"进程数: {len(psutil.pids())}")
```

3. **内存使用**
```python
import os
print(f"内存使用: {os.getpid()}")
```

## 📚 扩展阅读

- [Python multiprocessing 官方文档](https://docs.python.org/3/library/multiprocessing.html)
- [进程间通信最佳实践](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines)
- [性能优化指南](https://docs.python.org/3/library/multiprocessing.html#performance-considerations)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## �� 许可证

MIT License 