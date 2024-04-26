#include <iostream>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <limits>
#include <omp.h>

#define NUM_THREADS 2
#define N 13
#define START 0

using namespace std;

void print_path(vector<int>& path, bool include_start=false) {
    if (include_start) {
        cout << START << " ";
    }
    
    for(int x: path) {
        cout << x << " ";
    }
    
    if (include_start) {
        cout << START;
    }

    cout << endl;
}

double compute_cost(double* cost_matrix, vector<int>& perm_path) {
    double cost = 0.0;
    
    int prev_row = START;
    
    for(int i = 0; i < N - 1; i++) {
        int idx = prev_row * N + perm_path[i]; // row * cols + col
        cost += cost_matrix[idx];
        prev_row = perm_path[i];
    }

    cost += cost_matrix[prev_row * N + START]; // still have to get back to START

    return cost;
}


void find_best_path(double* cost_matrix) {
    vector<int> permutation_base;
    
    for(int i = 0, j = 0; i < N; i++) {
        if (i == START) continue;
        permutation_base.push_back(i);
    }
    
    double cost = std::numeric_limits<double>::max();
    vector<int> best_candidate_piece;
    
    // Each loop will be responsible for generating a different set of permutations.
    // The first position of the permutable vector is fixed, and each loop iteration will swap in
    // an element from index i+1 into this position. Each loop will then generate its own portion of permutations.
    #pragma omp parallel for num_threads(NUM_THREADS)
    for (int i = 0; i < N - 1; ++i) {
        // Make a copy of permutation_base
        auto perm = permutation_base;
        

        // rotate the i'th  element to the front. Keep the other elements sorted.
        rotate(perm.begin(), perm.begin() + i, perm.begin() + i + 1);
    
        // Now go through all permutations of the last `n-1` elements. 
        // Keep the first element fixed. 
        do {
            // #pragma omp critical (cs)
            // {
            //     print_path(perm);
            // }

            double local_cost = compute_cost(cost_matrix, perm);
            
            if (local_cost < cost) {
                #pragma omp critical (cs)
                {
                     if (local_cost < cost) {
                         cost = local_cost;
                         best_candidate_piece = perm;
                     }
                }
            }
        } while (next_permutation(perm.begin() + 1, perm.end()));
    }
    
    cout << "MIN COST: " << cost << endl;
    cout << "BEST PATH: "; print_path(best_candidate_piece, true);
}

void print_config() {
    cout << "CONFIG: -\n";
    cout << "NUM_THREADS=" << NUM_THREADS << ", N=" << N << ", START=" << START << endl << endl;
}

int main() {
    print_config();
    double start_time, end_time;
    double MAX_DOUBLE = numeric_limits<double>::max();
    
    double cost_matrix[N][N];
    
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++) {
            if (i != j) {
                cost_matrix[i][j] = (double)rand() / (double)RAND_MAX * (10.0 - 0.1) + 0.1;
            } else {
                cost_matrix[i][j] = MAX_DOUBLE;
            }
        }
    }
    
    start_time = omp_get_wtime();
    find_best_path(&cost_matrix[0][0]);
    end_time = omp_get_wtime();
    cout << "Execution time (in seconds): " << end_time - start_time << endl;

    return 0;
}