import random
import math

def simulated_annealing(puzzle, T_initial, alpha, stopping_temp):
    current_state = puzzle
    current_cost = cost(current_state)
    min_cost = current_cost
    min_state = current_stat
    
    T = T_initial
    
    while T > stopping_temp:
        new_state = swap(current_state.copy())
        new_cost = cost(new_state)

        if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / T):
            current_state = new_state
            current_cost = new_cost

            if current_cost < min_cost:
                min_cost = current_cost
                min_state = current_state
        
        T *= alpha 

    return min_state, min_cost

def cost(puzzle):
    cost = 0
    for i in range(512):
        for j in range(512):
            if (j + 1) % 128 == 0 and j + 1 < 512:
                cost += abs(int(puzzle[512 * i + j]) - int(puzzle[512 * i + j + 1]))
            if (i + 1) % 128 == 0 and i + 1 < 512:
                cost += abs(int(puzzle[512 * i + j]) - int(puzzle[512 * (i + 1) + j]))
    return cost

def swap(puzzle):
    indices = random.sample(range(16), 2)
    r1, r2 = indices[0] // 4, indices[1] // 4
    c1, c2 = indices[0] % 4, indices[1] % 4
    rn1, rn2 = 128 * r1, 128 * r2
    cn1, cn2 = 128 * c1, 128 * c2
    
    for i in range(128):
        for j in range(128):
            idx1 = (512 * (rn1 + i)) + (cn1 + j)
            idx2 = (512 * (rn2 + i)) + (cn2 + j)
            puzzle[idx1], puzzle[idx2] = puzzle[idx2], puzzle[idx1]

    return puzzle


with open('scrambled_lena.mat', 'r') as file:  
    puzzle = [line.strip() for line in file]

best_solution = None
min_cost = float('inf')


T_initial = 10000
alpha = 0.9
solution, cost = simulated_annealing(puzzle, T_initial, alpha, 0.1)

if cost < min_cost:
    min_cost = cost
    best_solution = solution

with open('solutioin.mat', 'w') as file:
    for item in best_solution:
        file.write(f"{item}\n")
