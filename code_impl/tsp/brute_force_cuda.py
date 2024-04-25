from numba import cuda
import numpy as np
import math

@cuda.jit
def calculate_distances(tours, distance_matrix, distances):
    idx = cuda.grid(1)
    if idx >= tours.shape[0]:
        return
    tour = tours[idx]
    total_distance = 0.0
    for i in range(1, tour.shape[0]):
        total_distance += distance_matrix[tour[i-1], tour[i]]
    total_distance += distance_matrix[tour[-1], tour[0]]
    distances[idx] = total_distance

def generate_permutations(num_cities):
    import itertools
    return np.array(list(itertools.permutations(range(num_cities))))

def run_cuda_tsp(distance_matrix):
    all_tours = generate_permutations(distance_matrix.shape[0])
    num_tours = all_tours.shape[0]

    # Move data to the device
    tours_device = cuda.to_device(all_tours)
    distance_matrix_device = cuda.to_device(distance_matrix)
    distances_device = cuda.device_array(num_tours, dtype=np.float32)

    # Setup blocks and threads
    threads_per_block = 64
    blocks_per_grid = math.ceil(num_tours / threads_per_block)

    # Run kernel
    calculate_distances[blocks_per_grid, threads_per_block](tours_device, distance_matrix_device, distances_device)

    # Get the results back
    distances = distances_device.copy_to_host()
    best_tour_idx = np.argmin(distances)
    best_distance = distances[best_tour_idx]
    return best_distance, all_tours[best_tour_idx]
