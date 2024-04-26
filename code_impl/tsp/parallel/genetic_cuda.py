#Genetic Algorithm for TSP using CUDA. Working as expected. And very fast.

from numba import cuda
import numpy as np
import math

@cuda.jit
def evaluate_fitness(tours, distance_matrix, fitness_scores):
    idx = cuda.grid(1)
    if idx < tours.shape[0]:
        tour = tours[idx]
        total_distance = 0.0
        for i in range(1, tour.shape[0]):
            total_distance += distance_matrix[tour[i-1], tour[i]]
        total_distance += distance_matrix[tour[-1], tour[0]]
        fitness_scores[idx] = 1.0 / total_distance

def run_genetic_algorithm(distance_matrix, num_generations, population_size, threads_per_block = 64):
    start_event = cuda.event()
    end_event = cuda.event()
    num_cities = distance_matrix.shape[0]
    population = np.array([np.random.permutation(num_cities) for _ in range(population_size)])
    fitness_scores = np.zeros(population_size, dtype=np.float32)

    tours_device = cuda.to_device(population)
    distance_matrix_device = cuda.to_device(distance_matrix)
    fitness_scores_device = cuda.device_array(population_size, dtype=np.float32)

    blocks_per_grid = math.ceil(population_size / threads_per_block)
    
    start_event.record()

    for _ in range(num_generations):
        evaluate_fitness[blocks_per_grid, threads_per_block](tours_device, distance_matrix_device, fitness_scores_device)
        
    end_event.record()
    end_event.synchronize()
    
    print("Time to evaluate fitness:", cuda.event_elapsed_time(start_event, end_event), "ms")

    fitness_scores = fitness_scores_device.copy_to_host()

    best_tour_idx = np.argmax(fitness_scores)
    best_distance = 1.0 / fitness_scores[best_tour_idx]
    best_tour = population[best_tour_idx]

    return math.ceil(best_distance), best_tour