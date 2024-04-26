from itertools import combinations as comb
import random
import sys


def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.
    
    Parameters:
        dists: distance matrix

    Returns:
        A tuple, (cost, path).
    """
    n = len(dists)
    memory = {}

    for k in range(1, n):
        memory[(1 << k, k)] = (dists[0][k], 0)

    for subset_size in range(2, n):
        for subset in comb(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((memory[(prev, m)][0] + dists[m][k], m))
                memory[(bits, k)] = min(res)

    bits = (2**n - 1) - 1

    res = []
    for k in range(1, n):
        res.append((memory[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = memory[(bits, parent)]
        bits = new_bits

    path.append(0)

    return opt, list(reversed(path))