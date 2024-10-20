import random
import sys

import numpy as np


def generate_distances(n):
    dists = np.zeros((n, n), dtype=np.float64)
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
    return np.array(dists, dtype=np.float64)


def get_argv(index, default):
    if len(sys.argv) > index:
        return sys.argv[index]
    return default


def data_handler(input_data):
    if input_data.endswith('.csv'):
        # Assuming read_distances is implemented appropriately
        dists = np.array(read_distances(input_data), dtype=np.float64)
    else:
        n = int(input_data)
        dists = generate_distances(n)

    return dists
