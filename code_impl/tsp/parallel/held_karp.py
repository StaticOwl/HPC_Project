# Somewhat working. But not as parallel as it should be.

import numpy as np
from numba import njit, prange, config

config.THREADING_LAYER = 'omp'


@njit
def count_set_bits(x):
    count = 0
    while x:
        count += x & 1
        x >>= 1
    return count


@njit
def get_parent(memory, bits, k):
    if (bits, k) in memory:
        return memory[(bits, k)]
    else:
        return (np.inf, -1)


@njit
def manual_argmin(array):
    min_value = np.inf
    min_index = -1
    for i in range(len(array)):
        # Assume the first element of the tuple holds the value to compare
        if array[i][0] < min_value:
            min_value = array[i][0]
            min_index = i
    return min_index


@njit(parallel=True, debug=True)
def held_karp(dists):
    n = dists.shape[0]
    memory = dict()

    # Initialize memory for subsets of size 1
    for k in prange(1, n):
        memory[(1 << k, k)] = (dists[0, k], 0)

    # Compute optimal cost and parent for all subsets of size 2 to n
    for subset_size in range(2, n):
        for subset_int in range(1, 1 << n):
            if count_set_bits(subset_int) == subset_size and (subset_int & 1) == 0:
                bits = subset_int
                for k in range(1, n):
                    if bits & (1 << k):
                        prev = bits & ~(1 << k)
                        res = []
                        for m in range(1, n):
                            if m != k and (prev & (1 << m)):
                                res.append((memory[(prev, m)][0] + dists[m, k], m))
                        if res:
                            res = np.array(res, dtype=np.int64)
                            idx = np.argmin(res[:, 0])
                            memory[(bits, k)] = (res[idx, 0], res[idx, 1])

    # Find the optimal cost and reconstruct the optimal path
    bits = (1 << n) - 2
    res2 = []
    for k in range(1, n):
        opt, parent = get_parent(memory, bits, k)
        res2.append((opt + dists[k, 0], np.int64(k)))

    idx = manual_argmin(res2)
    opt, last = res2[idx]

    return opt, last
