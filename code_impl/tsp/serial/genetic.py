import numpy as np
import time
import math

def evaluate_fitness(tours, distance_matrix):
    num_tours = tours.shape[0]
    fitness_scores = np.zeros(num_tours, dtype=np.float32)
    for idx in range(num_tours):
        tour = tours[idx]
        total_distance = 0.0
        for i in range(1, len(tour)):
            total_distance += distance_matrix[tour[i-1], tour[i]]
        total_distance += distance_matrix[tour[-1], tour[0]]
        fitness_scores[idx] = 1.0 / total_distance
    return fitness_scores

def run_genetic_algorithm(distance_matrix, num_generations, population_size):
    num_cities = distance_matrix.shape[0]
    population = np.array([np.random.permutation(num_cities) for _ in range(population_size)])
    
    start_time = time.time()

    for _ in range(num_generations):
        fitness_scores = evaluate_fitness(population, distance_matrix)

    end_time = time.time()
    print("Time to evaluate fitness:", (end_time - start_time) * 1000, "ms")

    best_tour_idx = np.argmax(fitness_scores)
    best_distance = 1.0 / fitness_scores[best_tour_idx]
    best_tour = population[best_tour_idx]

    return math.ceil(best_distance), best_tour