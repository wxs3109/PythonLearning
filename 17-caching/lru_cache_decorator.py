# LRU Cache Decorator


from functools import lru_cache


@lru_cache(maxsize=10)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def fibonacci_matrix_multiplication(n):
    matrix = [[1, 1], [1, 0]]
    np.linalg.matrix_power(matrix, n)