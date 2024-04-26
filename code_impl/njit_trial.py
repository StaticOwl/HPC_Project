from numba import njit
from numba.openmp import openmp_context as omp
from numba.openmp import omp_get_wtime, omp_get_thread_num, omp_get_num_threads
from numba import extending, types

#import to print floats in njit
from utils import str_float


@njit
def pi_loop():
    num_steps = 1000000
    step = 1.0 / num_steps
    the_sum = 0.0
    start_time = omp_get_wtime()
    with omp("parallel private(x)"):
        print(f"Thread: {omp_get_thread_num()}")
        with omp("for reduction(+:the_sum) schedule(static) private(x)"):
            for j in range(num_steps):
                x = (j + 0.5) * step
                the_sum += 4.0 / (1.0 + x * x)
                
    pi = step * the_sum
    runtime = omp_get_wtime() - start_time
    print(f"Threads: {(omp_get_num_threads())}, Pi: {str(pi)}, Time: {str(runtime)}")
        
pi_loop()