# ============================================================
# 📘 asyncio I/O Operations
# ============================================================

import asyncio
import aiofiles
import aiohttp
import tempfile
import os

# 1. 异步文件操作
# Knowledge:
# - 使用 aiofiles 进行异步文件 I/O
# - 非阻塞的文件读写
# - 支持上下文管理器

async def demo_file_operations():
    print("=== 异步文件操作示例 ===")
    
    # 写入文件
    async with aiofiles.open('test.txt', 'w') as f:
        await f.write('Hello, Async World!\n')
        await f.write('这是异步文件操作\n')
    
    print("文件写入完成")
    
    # 读取文件
    async with aiofiles.open('test.txt', 'r') as f:
        content = await f.read()
        print(f"文件内容:\n{content}")
    
    # 逐行读取
    async with aiofiles.open('test.txt', 'r') as f:
        async for line in f:
            print(f"行: {line.strip()}")
    
    # 清理
    os.remove('test.txt')

# 2. 异步 HTTP 请求
# Knowledge:
# - 使用 aiohttp 进行异步 HTTP 请求
# - 支持会话管理
# - 并发请求

async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        return f"Error fetching {url}: {e}"

async def demo_http_requests():
    print("=== 异步 HTTP 请求示例 ===")
    
    urls = [
        'http://httpbin.org/delay/1',
        'http://httpbin.org/delay/2',
        'http://httpbin.org/delay/1'
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for i, result in enumerate(results):
            print(f"URL {i+1} 响应长度: {len(result)}")

# 3. 异步流处理
# Knowledge:
# - 处理大文件
# - 内存高效的流式处理
# - 支持管道操作

async def process_large_file():
    print("=== 异步流处理示例 ===")
    
    # 创建大文件
    with open('large_file.txt', 'w') as f:
        for i in range(1000):
            f.write(f"Line {i}: This is a test line with some content.\n")
    
    # 异步处理大文件
    processed_lines = 0
    async with aiofiles.open('large_file.txt', 'r') as f:
        async for line in f:
            # 模拟处理
            processed_line = line.upper().strip()
            processed_lines += 1
            
            if processed_lines % 100 == 0:
                print(f"已处理 {processed_lines} 行")
    
    print(f"总共处理了 {processed_lines} 行")
    
    # 清理
    os.remove('large_file.txt')

# 4. 异步数据库操作
# Knowledge:
# - 模拟异步数据库连接
# - 连接池管理
# - 事务处理

class AsyncDatabase:
    def __init__(self):
        self.connections = []
    
    async def connect(self):
        # 模拟连接延迟
        await asyncio.sleep(0.1)
        connection_id = len(self.connections) + 1
        self.connections.append(connection_id)
        print(f"数据库连接 {connection_id} 已建立")
        return connection_id
    
    async def query(self, connection_id, sql):
        await asyncio.sleep(0.2)  # 模拟查询时间
        print(f"连接 {connection_id} 执行查询: {sql}")
        return f"查询结果: {sql}"
    
    async def close(self, connection_id):
        if connection_id in self.connections:
            self.connections.remove(connection_id)
            print(f"数据库连接 {connection_id} 已关闭")

async def demo_database():
    print("=== 异步数据库操作示例 ===")
    
    db = AsyncDatabase()
    
    # 并发执行多个查询
    async def database_worker(worker_id):
        conn_id = await db.connect()
        try:
            result = await db.query(conn_id, f"SELECT * FROM users WHERE id = {worker_id}")
            print(f"Worker {worker_id}: {result}")
        finally:
            await db.close(conn_id)
    
    # 创建多个数据库工作器
    tasks = [database_worker(i) for i in range(3)]
    await asyncio.gather(*tasks)

# 5. 异步 WebSocket
# Knowledge:
# - 实时双向通信
# - 消息处理
# - 连接管理

async def websocket_client():
    print("=== 异步 WebSocket 示例 ===")
    
    # 模拟 WebSocket 连接
    uri = "ws://echo.websocket.org"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(uri) as ws:
                print("WebSocket 连接已建立")
                
                # 发送消息
                await ws.send_str("Hello, WebSocket!")
                
                # 接收消息
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        print(f"收到消息: {msg.data}")
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print(f"WebSocket 错误: {ws.exception()}")
                        break
    except Exception as e:
        print(f"WebSocket 连接失败: {e}")

# 6. 异步管道操作
# Knowledge:
# - 数据流处理
# - 管道模式
# - 数据转换

async def data_producer():
    for i in range(5):
        await asyncio.sleep(0.5)
        yield f"数据 {i}"

async def data_processor(data):
    await asyncio.sleep(0.1)
    return f"处理后的 {data}"

async def data_consumer(processed_data):
    print(f"消费: {processed_data}")

async def demo_pipeline():
    print("=== 异步管道操作示例 ===")
    
    async for data in data_producer():
        processed = await data_processor(data)
        await data_consumer(processed)

# 7. 异步日志记录
# Knowledge:
# - 异步日志写入
# - 日志轮转
# - 性能优化

class AsyncLogger:
    def __init__(self, filename):
        self.filename = filename
        self.queue = asyncio.Queue()
        self.running = True
    
    async def start(self):
        # 启动日志写入任务
        asyncio.create_task(self._writer())
    
    async def log(self, message):
        await self.queue.put(f"{asyncio.get_event_loop().time()}: {message}\n")
    
    async def _writer(self):
        async with aiofiles.open(self.filename, 'a') as f:
            while self.running:
                try:
                    message = await asyncio.wait_for(self.queue.get(), timeout=1)
                    await f.write(message)
                    await f.flush()
                except asyncio.TimeoutError:
                    continue
    
    async def stop(self):
        self.running = False
        await self.queue.join()

async def demo_logging():
    print("=== 异步日志记录示例 ===")
    
    logger = AsyncLogger('async.log')
    await logger.start()
    
    # 并发记录日志
    tasks = []
    for i in range(10):
        task = asyncio.create_task(logger.log(f"日志消息 {i}"))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    await logger.stop()
    
    # 读取日志
    async with aiofiles.open('async.log', 'r') as f:
        content = await f.read()
        print("日志内容:")
        print(content)
    
    # 清理
    os.remove('async.log')

# 8. 实际应用 - 异步文件下载器
# Knowledge:
# - 并发下载
# - 进度跟踪
# - 错误处理

async def download_file(session, url, filename):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(filename, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        await f.write(chunk)
                print(f"文件 {filename} 下载完成")
                return True
            else:
                print(f"下载失败 {url}: {response.status}")
                return False
    except Exception as e:
        print(f"下载错误 {url}: {e}")
        return False

async def demo_downloader():
    print("=== 异步文件下载器示例 ===")
    
    urls = [
        ('http://httpbin.org/bytes/1024', 'file1.bin'),
        ('http://httpbin.org/bytes/2048', 'file2.bin'),
        ('http://httpbin.org/bytes/512', 'file3.bin')
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_file(session, url, filename)
            for url, filename in urls
        ]
        
        results = await asyncio.gather(*tasks)
        success_count = sum(results)
        print(f"成功下载 {success_count}/{len(urls)} 个文件")
    
    # 清理下载的文件
    for _, filename in urls:
        if os.path.exists(filename):
            os.remove(filename)

# 主函数
async def main():
    print("📁 asyncio I/O 操作演示")
    print("=" * 50)
    
    await demo_file_operations()
    print()
    
    await demo_http_requests()
    print()
    
    await process_large_file()
    print()
    
    await demo_database()
    print()
    
    await websocket_client()
    print()
    
    await demo_pipeline()
    print()
    
    await demo_logging()
    print()
    
    await demo_downloader()
    print()
    
    print("✅ 所有 I/O 操作演示完成")

if __name__ == "__main__":
    asyncio.run(main()) 