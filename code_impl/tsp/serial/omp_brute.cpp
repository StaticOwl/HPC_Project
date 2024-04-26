#include <iostream>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <limits>
#include <omp.h>

#define N 15
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
    vector<int> perm;
    
    for(int i = 0, j = 0; i < N; i++) {
        if (i == START) continue;
        perm.push_back(i);
    }
    
    double cost = std::numeric_limits<double>::max();
    vector<int> best_candidate_piece;
                
    
    // Go through all permutations of the 'n` elements.
    do {
        // print all possible permutation paths
        // print_path(perm);

        double local_cost = compute_cost(cost_matrix, perm);
        
        if (local_cost < cost) {
            if (local_cost < cost) {
                cost = local_cost;
                best_candidate_piece = perm;
            }
        }
    } while (next_permutation(perm.begin(), perm.end()));

    
    cout << "MIN COST: " << cost << endl;
    cout << "BEST PATH: "; print_path(best_candidate_piece, true);
}



int main() {
    double start_time, end_time;
    double MAX_DOUBLE = numeric_limits<double>::max();
    
    double cost_matrix[N][N];
    
    // double cost_matrix[N][N] = {
    //     {MAX_DOUBLE, 20, 30, 10, 11},
    //     {15, MAX_DOUBLE, 16, 4, 2},
    //     {3, 5, MAX_DOUBLE, 2, 4},
    //     {19, 6, 18, MAX_DOUBLE, 3},
    //     {16, 4, 7, 16, MAX_DOUBLE}
    // };
    
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