# ============================================================
# 📘 Multiprocessing Basics
# ============================================================

import multiprocessing
import time

def worker(num):
    print(f"Worker {num} starting")
    time.sleep(2)
    print(f"Worker {num} finished")

if __name__ == "__main__":
    processes = []

    # print the number of cores
    print(f"Number of cores: {multiprocessing.cpu_count()}")

    # Launch 4 worker processes
    for i in range(4):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    # Wait for all to complete
    for p in processes:
        p.join()

    print("All workers done")
