from numba import njit, prange
import numpy as np
import sys

@njit(parallel=True)
def brute_force_tsp(distance_matrix):
    print(distance_matrix.dtype)
    num_cities = distance_matrix.shape[0]
    min_distance = np.array([sys.maxsize], dtype=np.int64)
    best_tour = np.zeros(num_cities, dtype=np.int64)

    for i in prange(num_cities):
        tour = np.zeros(num_cities, dtype=np.int64)
        visited = np.zeros(num_cities, dtype=np.bool_)
        visited[i] = True
        tour[0] = np.int64(i)
        tsp_util(distance_matrix, visited, tour, 1, 0, min_distance, best_tour)

    return best_tour, min_distance

@njit(parallel=True)
def tsp_util(distance_matrix, visited, tour, depth, cur_distance, min_distance, best_tour):
    if depth == len(visited):
        if cur_distance + distance_matrix[tour[-1], tour[0]] < min_distance[0]:
            min_distance[0] = cur_distance + distance_matrix[tour[-1], tour[0]]
            best_tour[:] = tour[:]
        return

    for i in prange(len(visited)):
        if not visited[i]:
            new_distance = cur_distance + distance_matrix[tour[depth - 1], i]
            if new_distance < min_distance[0]:
                visited[i] = True
                tour[depth] = i
                tsp_util(distance_matrix, visited, tour, depth + 1, new_distance, min_distance, best_tour)
                visited[i] = False
