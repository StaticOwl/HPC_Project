import numpy as np
from numba import cuda
# from numba.types import int32, float32
from numba.cuda.types import types
import math

# Define a large float value to represent infinity
INF = 1e30

# Define the Lin-Kernighan heuristic kernel
@cuda.jit
def lin_kernighan_kernel(d_matrix, tour, best_tour, best_length, iterations):
    # Get the thread's unique index
    idx = cuda.grid(1)

    # Initialize shared memory for storing 2-opt moves and deltas
    shared_moves = cuda.shared.array(shape=(2, 2), dtype=types.int32)
    shared_deltas = cuda.shared.array(shape=(2), dtype=types.float32)

    # Initialize per-thread variables
    local_best_length = INF
    local_best_move = (-1, -1)

    # Iterate over a subset of potential moves
    for i in range(idx, len(tour)):
        for j in range(i + 2, len(tour)):
            # Swap two edges to create a potential move
            move = (i, j)

            # Evaluate the move (calculate delta)
            delta = evaluate_move(d_matrix, tour, move)

            # Update the local best move if necessary
            if delta < local_best_length:
                local_best_length = delta
                local_best_move = move

    # Store the best move and its delta in shared memory
    shared_moves[0, idx] = local_best_move[0]
    shared_moves[1, idx] = local_best_move[1]
    shared_deltas[idx] = local_best_length

    # Synchronize threads to ensure all moves and deltas are stored
    cuda.syncthreads()

    # Reduce to find the global best move and its delta
    if idx == 0:
        global_best_length:types.float64 = INF
        global_best_move = (-1, -1)
        for i in range(len(tour)):
            if shared_deltas[i] < global_best_length:
                global_best_length = shared_deltas[i]
                global_best_move = (shared_moves[0, i], shared_moves[1, i])
        
                
        #Apply the best move to update the tour if it improves
        if global_best_length < best_length:
            tour[global_best_move[0]], tour[global_best_move[1]] = tour[global_best_move[1]], tour[global_best_move[0]]
            best_length = global_best_length
            for i in range(len(tour)):
                best_tour[i] = tour[i]

    # Wait for all threads to finish
    cuda.syncthreads()

# Evaluate the change in tour length if a 2-opt move is applied
@cuda.jit(device=True)
def evaluate_move(d_matrix, tour, move):
    i, j = move
    n = len(tour)

    # Calculate the change in tour length
    delta = 0.0
    if i == 0 and j == n - 1:
        delta -= d_matrix[tour[n - 1], tour[0]] + d_matrix[tour[n - 2], tour[1]]
        delta += d_matrix[tour[n - 2], tour[0]] + d_matrix[tour[n - 1], tour[1]]
    elif j == i + 1:
        delta -= d_matrix[tour[i], tour[i + 1]] + d_matrix[tour[j], tour[(j + 1) % n]]
        delta += d_matrix[tour[i], tour[j]] + d_matrix[tour[i + 1], tour[(j + 1) % n]]
    else:
        delta -= d_matrix[tour[i], tour[(i + 1) % n]] + d_matrix[tour[j], tour[(j + 1) % n]]
        delta += d_matrix[tour[i], tour[j]] + d_matrix[tour[(i + 1) % n], tour[(j + 1) % n]]

    return delta

# Lin-Kernighan heuristic function
def lin_kernighan(d_matrix, iterations=1000):
    # Initialize the tour with a simple greedy algorithm
    n = len(d_matrix)
    tour = np.arange(n, dtype=np.int32)
    best_tour = tour.copy()
    best_length = calculate_tour_length(d_matrix, best_tour)

    # Set up CUDA grid and block dimensions
    threads_per_block = 256
    blocks_per_grid = math.ceil(n / threads_per_block)

    # Copy data to device memory
    d_d_matrix = cuda.to_device(d_matrix)
    d_tour = cuda.to_device(tour)
    d_best_tour = cuda.to_device(best_tour)
    d_best_length = cuda.to_device(best_length)

    # Run Lin-Kernighan kernel
    for _ in range(iterations):
        lin_kernighan_kernel[blocks_per_grid, threads_per_block](d_d_matrix, d_tour, d_best_tour, d_best_length, iterations)

    # Copy results back to host
    best_tour = d_best_tour.copy_to_host()
    best_length = d_best_length.copy_to_host()

    return best_tour, best_length

# Function to calculate the length of a tour
def calculate_tour_length(d_matrix, tour):
    length = 0.0
    n = len(tour)
    for i in range(n):
        length += d_matrix[tour[i], tour[(i + 1) % n]]
    return length