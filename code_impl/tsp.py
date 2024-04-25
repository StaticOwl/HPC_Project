from numba import threading_layer, set_num_threads
import numpy as np
import random
import sys
import time

from tsp.held_karp import held_karp
from tsp.two_opt import two_opt
from tsp.cuda_try import lin_kernighan
from tsp.brute_force import brute_force_tsp
from tsp.brute_force_cuda import run_cuda_tsp
from tsp.genetic_cuda import run_genetic_algorithm

set_num_threads(14)

def generate_distances(n):
    dists = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        for j in range(i + 1, n):
            dist = random.randint(1, 99)
            dists[i, j] = dist
            dists[j, i] = dist
    return dists


def read_distances(filename):
    """
    Read a CSV file containing distance matrices for the Traveling Salesman Problem.
    
    Parameters:
        filename: The path to a CSV file containing the distance matrix.

    Returns:
        A Numpy array of the distances.
    """
    dists = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                # Split the line by comma, strip whitespace, convert to integers
                row = list(map(int, map(str.strip, line.split(','))))
                dists.append(row)
    return np.array(dists, dtype=np.int64)

def get_argv(index, default):
    if len(sys.argv) > index:
        return sys.argv[index]
    return default

if __name__ == '__main__':
    start_time = time.time()
    arg = get_argv(1, 10)
    num_threads = int(get_argv(2, 64))
    if arg.endswith('.csv'):
        # Assuming read_distances is implemented appropriately
        dists = np.array(read_distances(arg), dtype=np.float32)
    else:
        n = int(arg)
        dists = generate_distances(n)

    for row in dists:
        print(' '.join(f"{int(n):3d}" for n in row))
    print('')
    
    print("Data Generation Time:", time.time() - start_time, "s")
    tsp_start_time = time.time()
    cost, path = two_opt(dists)
    print("Cost:", cost)
    print("Path:", path)
    print("TSP Algorithm Time:", time.time() - tsp_start_time, "s")
    print("Total Time:", time.time() - start_time, "s")
