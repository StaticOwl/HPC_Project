import argparse
import time
import utils.data_handler as dh
from numba import set_num_threads

from tsp import parallel as p
from tsp import serial as s

def print_matrix(dists, noout=False):
    if noout:
        return
    for row in dists:
        print(' '.join(f"{int(n):3d}" for n in row))
    print('')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run TSP algorithms with different modes and settings.')
    parser.add_argument('--type', default='serial', choices=['serial', 'parallel'], help='Execution type (serial or parallel)')
    parser.add_argument('--algo', default='held_karp', choices=['held_karp', 'two_opt', 'brute_force', 'genetic'], help='Algorithm to use for solving TSP')
    parser.add_argument('--input_size', default=10, help='Size of the input data')
    parser.add_argument('--num_threads', default=64, type=int, help='Number of threads to use (applicable in parallel mode)')
    parser.add_argument('--noout', default=False, action='store_true', help='Do not print the output')
    return parser.parse_args()

def main(args=None):
    start_time = time.time()
    
    if args is None:
        print("You have to pass some arguments. Run 'python tsp.py --help' for more information.")
    
    cost, path = 0, []
    try:
        dists = dh.data_handler(args.input_size)
        print_matrix(dists, args.noout)
        print("Data Generation Time:", time.time() - start_time, "s")
        
        tsp_start_time = time.time()
        if args.type == "parallel":
            if args.algo not in ["brute_force_cuda", "genetic"]:
                set_num_threads(args.num_threads)
            if args.algo == "held_karp":
                cost, path = p.held_karp(dists) # check once
            elif args.algo == "two_opt":
                cost, path = p.two_opt(dists) # Not actual value always
            elif args.algo == "brute_force":
                cost, path = p.run_cuda_tsp(dists)
            elif args.algo == "genetic":
                cost, path = p.run_genetic_algorithm(dists, 100, 50, args.num_threads)
            else:
                raise ValueError(f"Unknown algorithm '{args.algo}'")
        elif args.type == "serial":
            if args.algo == "held_karp":
                cost, path = s.held_karp(dists)
            elif args.algo == "two_opt":
                cost, path = s.two_opt(dists) # Not actual value always
            elif args.algo == "brute_force":
                cost, path = s.run_tsp(dists)
            elif args.algo == "genetic":
                cost, path = s.run_genetic_algorithm(dists, 100, 50)
            else:
                raise ValueError(f"Unknown algorithm '{args.algo}'")
        else:
            raise ValueError(f"Unknown type '{args.type}'")
        
        print("Cost:", cost)
        print("Path:", path)
        print("TSP Algorithm Time:", time.time() - tsp_start_time, "s")

    except Exception as e:
        print("An error occurred:", e)

    print("Total Time:", time.time() - start_time, "s")

if __name__ == '__main__':
    main(parse_arguments())
