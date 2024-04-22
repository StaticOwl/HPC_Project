# Not Working

import numpy as np
from numba import njit, prange, float32, uint64
from math import sqrt
from numba.typed import Dict, List
from numba.core import types
import itertools

@njit(parallel=True)
def generate_distance_matrix(cities):
    n = len(cities)
    dMatrix = np.zeros((n, n), dtype=np.float32)
    for i in prange(n):
        for j in prange(n):
            if i != j:
                dx = cities[i][0] - cities[j][0]
                dy = cities[i][1] - cities[j][1]
                dMatrix[i][j] = sqrt(dx * dx + dy * dy)
    return dMatrix

@njit
def generate_subsets(n, k):
    result = List()
    # Start with the smallest lexicographical combination
    combo = np.arange(k, dtype=np.int32)
    while True:
        result.append(combo.copy())
        # Move to the next combination
        # Find the first item that is not its maximum
        for i in range(k)[::-1]:
            if combo[i] != i + n - k:
                break
        else:
            # If no break, then this is the last combination
            return result
        # Increment this item
        combo[i] += 1
        # Make all subsequent items the smallest possible
        for j in range(i + 1, k):
            combo[j] = combo[j - 1] + 1
    return result

@njit
def compute_key(set, z):
    key = uint64(z)
    for item in set:
        key |= uint64(1) << uint64(item + 8)
    return key

@njit(parallel=True)
def tsp_solve(distance_matrix):
    n = len(distance_matrix)
    costs = Dict.empty(
        key_type=types.uint64,
        value_type=types.float32
    )

    # Initialize direct distances from the starting point
    for i in prange(1, n):
        key = compute_key((0,), i)
        costs[key] = distance_matrix[0][i]

    # Dynamic programming to compute the costs of all routes
    for s in range(2, n+1):
        subsets = generate_subsets(n, s)
        for subset in subsets:
            if 0 not in subset:  # Ensure starting point is in the subset
                continue
            for z in subset:
                if z == 0:
                    continue
                # Avoid using a generator here
                set_without_z = []
                for x in subset:
                    if x != z:
                        set_without_z.append(x)
                set_without_z = tuple(set_without_z)
                key = compute_key(set_without_z, z)
                min_cost = float32('inf')
                for k in set_without_z:
                    if k == 0:
                        continue
                    current_key = compute_key(set_without_z, k)
                    cost = costs[current_key] + distance_matrix[k][z]
                    if cost < min_cost:
                        min_cost = cost
                costs[key] = min_cost

    # Find the minimum cost to complete the tour
    min_path_cost = float32('inf')
    final_set = tuple(range(1, n))
    for k in final_set:
        key = compute_key(final_set, k)
        cost = costs[key] + distance_matrix[k][0]
        if cost < min_path_cost:
            min_path_cost = cost

    return min_path_cost

# Define cities and solve TSP
cities = [(0, 0), (1, 2), (3, 1), (6, 5)]
distance_matrix = generate_distance_matrix(np.array(cities))
min_cost = tsp_solve(distance_matrix)
print(f"Minimum travel cost: {min_cost}")
