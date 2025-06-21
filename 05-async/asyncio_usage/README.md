# asyncio 使用指南

这个目录包含了 `asyncio` 模块的详细使用示例和最佳实践。

## 文件结构

```
asyncio_usage/
├── README.md              # 本文件
├── 01_core_functions.py   # 核心函数使用
├── 02_synchronization.py  # 同步原语
└── 03_io_operations.py    # I/O 操作
```

## 学习路径

### 1. 核心函数 (01_core_functions.py)
- `asyncio.run()` - 运行协程的主函数
- 事件循环管理
- 任务创建和管理
- 并发执行 (`gather`, `wait`)
- 超时控制
- 任务取消

### 2. 同步原语 (02_synchronization.py)
- **Lock** - 异步锁
- **Semaphore** - 信号量
- **Event** - 事件
- **Condition** - 条件变量
- **Barrier** - 屏障
- **Queue** - 异步队列
- 连接池示例

### 3. I/O 操作 (03_io_operations.py)
- 异步文件操作 (`aiofiles`)
- 异步 HTTP 请求 (`aiohttp`)
- 异步流处理
- 异步数据库操作
- WebSocket 通信
- 管道操作
- 异步日志记录
- 文件下载器

## 运行示例

### 安装依赖
```bash
pip install aiofiles aiohttp
```

### 运行单个文件
```bash
python 01_core_functions.py
python 02_synchronization.py
python 03_io_operations.py
```

### 运行所有示例
```bash
for file in *.py; do
    if [ "$file" != "README.md" ]; then
        echo "运行 $file..."
        python "$file"
        echo "完成 $file"
        echo "---"
    fi
done
```

## 关键概念

### 协程 (Coroutine)
- 使用 `async def` 定义的函数
- 可以暂停和恢复执行
- 使用 `await` 等待其他协程

### 任务 (Task)
- 协程的调度单元
- 可以并发执行
- 可以取消和监控

### 事件循环 (Event Loop)
- 协程的执行环境
- 管理所有异步操作
- 处理 I/O 事件

### 同步原语
- 用于协程间的同步
- 防止竞态条件
- 控制资源访问

## 最佳实践

1. **总是使用 `asyncio.run()`** 运行主协程
2. **避免在协程中使用阻塞操作**
3. **使用适当的同步原语** 管理共享资源
4. **正确处理异常** 和取消操作
5. **使用连接池** 管理数据库连接
6. **设置合理的超时** 避免无限等待

## 常见错误

1. **忘记 await**
   ```python
   # 错误
   asyncio.sleep(1)
   
   # 正确
   await asyncio.sleep(1)
   ```

2. **在协程中使用阻塞 I/O**
   ```python
   # 错误
   time.sleep(1)
   
   # 正确
   await asyncio.sleep(1)
   ```

3. **没有处理异常**
   ```python
   # 错误
   await risky_operation()
   
   # 正确
   try:
       await risky_operation()
   except Exception as e:
       print(f"操作失败: {e}")
   ```

## 性能优化

1. **使用连接池** 复用连接
2. **批量操作** 减少 I/O 次数
3. **适当的并发度** 避免资源过载
4. **使用 `gather` 而不是循环 await**
5. **及时取消不需要的任务**

## 调试技巧

1. **启用调试模式**
   ```python
   asyncio.get_event_loop().set_debug(True)
   ```

2. **使用 `asyncio.current_task()`** 获取当前任务
3. **监控任务状态** 使用 `task.done()` 和 `task.result()`
4. **使用日志记录** 跟踪异步操作

## 扩展阅读

- [Python asyncio 官方文档](https://docs.python.org/3/library/asyncio.html)
- [aiofiles 文档](https://github.com/Tinche/aiofiles)
- [aiohttp 文档](https://docs.aiohttp.org/)
- [异步编程最佳实践](https://docs.python.org/3/library/asyncio-dev.html) 