# This is so far the fastest implementation. But it is different than help-karp. Also this is giving different output different times.

from numba import njit, config, prange, set_num_threads
import numpy as np

config.THREADING_LAYER = 'omp'

set_num_threads(14)

@njit
def calculate_distance(tour, distance_matrix):
    total_distance = 0.0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i], tour[i + 1]]
    total_distance += distance_matrix[tour[-1], tour[0]]  # Complete the tour
    return total_distance

@njit(parallel=True)
def get_tour(tour, distance_matrix):
    n = len(tour)
    improvement = True
    while improvement:
        improvement = False
        # The outer loop can be parallelized since each iteration is independent in the 2-opt swaps
        for i in prange(1, n - 2):
            for j in range(i + 2, n):
                if j - i == 1: continue  # Skip adjacent edges
                new_tour = tour.copy()
                new_tour[i:j] = tour[j - 1:i - 1:-1]  # Reverse the segment between i and j
                print("New Distance: ", calculate_distance(new_tour, distance_matrix))
                print("Old Distance: ", calculate_distance(tour, distance_matrix))
                if calculate_distance(new_tour, distance_matrix) < calculate_distance(tour, distance_matrix):
                    tour[:] = new_tour
                    improvement = True
    return tour

@njit(parallel=True)
def two_opt(dists):
    init_tour = np.arange(dists.shape[0])
    np.random.shuffle(init_tour)
    
    print("Initial tour:", init_tour)
    
    optimized_tour = get_tour(init_tour, dists)
    optimized_distance = calculate_distance(optimized_tour, dists)
    
    return optimized_distance, optimized_tour