import numpy as np

def calculate_distance(tour, distance_matrix):
    total_distance = 0.0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i], tour[i + 1]]
    total_distance += distance_matrix[tour[-1], tour[0]]  # Complete the tour
    return total_distance

def get_tour(tour, distance_matrix):
    n = len(tour)
    improvement = True
    while improvement:
        improvement = False
        for i in range(1, n - 2):
            for j in range(i + 2, n):
                if j - i == 1: continue  # Skip adjacent edges
                new_tour = tour.copy()
                new_tour[i:j] = tour[j - 1:i - 1:-1]  # Reverse the segment between i and j
                if calculate_distance(new_tour, distance_matrix) < calculate_distance(tour, distance_matrix):
                    tour[:] = new_tour
                    improvement = True
    return tour

def two_opt(dists):
    init_tour = np.arange(dists.shape[0])
    np.random.shuffle(init_tour)
    
    optimized_tour = get_tour(init_tour, dists)
    optimized_distance = calculate_distance(optimized_tour, dists)
    
    return optimized_distance, optimized_tour