import numpy as np

if __name__ == '__main__':
    a = np.array([1, 2, 3], dtype=complex)
    print(a[1])
    dt = np.dtype(np.int32)
    print(dt)

    a = np.arange(24)
    print(a.ndim)  # a 现只有一个维度
    # 现在调整其大小
    b = a.reshape(2, 4, 3)  # b 现在拥有三个维度
    print(b)
