import numpy as np
import itertools

def calculate_distances(tours, distance_matrix):
    num_tours = tours.shape[0]
    distances = np.zeros(num_tours, dtype=np.float32)
    for idx in range(num_tours):
        tour = tours[idx]
        total_distance = 0.0
        for i in range(1, len(tour)):
            total_distance += distance_matrix[tour[i-1], tour[i]]
        total_distance += distance_matrix[tour[-1], tour[0]]
        distances[idx] = total_distance
    return distances

def generate_permutations(num_cities):
    return np.array(list(itertools.permutations(range(num_cities))))

def run_tsp(distance_matrix):
    all_tours = generate_permutations(distance_matrix.shape[0])
    distances = calculate_distances(all_tours, distance_matrix)
    best_tour_idx = np.argmin(distances)
    best_distance = distances[best_tour_idx]
    return best_distance, all_tours[best_tour_idx]