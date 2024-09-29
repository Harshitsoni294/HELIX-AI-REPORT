import math
import random
import time
import os

def dist(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def total_dist(tour):
    return sum(dist(tour[i], tour[(i + 1) % len(tour)]) for i in range(len(tour)))

def sim_anneal(cities, temp=10000, cool=0.90, stop_temp=1e-8, stop_iter=1000000):
    cur_tour = cities[:]
    best_tour = cur_tour[:]
    n = len(cities)
    
    it = 1
    while temp > stop_temp and it < stop_iter:
        i, j = sorted(random.sample(range(n), 2))
        new_tour = cur_tour[:]
        new_tour[i:j + 1] = reversed(new_tour[i:j + 1])
        
        cur_dist = total_dist(cur_tour)
        new_dist = total_dist(new_tour)
        
        if new_dist < cur_dist:
            cur_tour = new_tour
            if new_dist < total_dist(best_tour):
                best_tour = new_tour
        elif random.random() < math.exp((cur_dist - new_dist) / temp):
            cur_tour = new_tour
        
        temp *= cool
        it += 1
    
    return best_tour, total_dist(best_tour)

def read_tsp(fp):
    cities = []
    with open(fp, 'r') as file:
        for line in file:
            if line.strip().isdigit():
                break
        for line in file:
            if line.strip() == "EOF":
                break
            parts = line.strip().split()
            if len(parts) == 3 and parts[0].isdigit():
                cities.append((float(parts[1]), float(parts[2])))
    return cities

def solve_tsp(name, cities):
    start = time.time()
    best_tour, best_dist = sim_anneal(cities)
    end = time.time()
    
    return best_dist, end - start

files = [
    "xqf131.tsp",
    "xqg237.tsp",
    "pbk411.tsp",
    "pbn423.tsp",
    "pka379.tsp",
    "pma343.tsp",
]

results = {}

for file in files:
    if os.path.exists(file):
        cities = read_tsp(file)
        name = os.path.splitext(file)[0]
        results[name] = solve_tsp(name, cities)
    else:
        print(f"File not found: {file}")

print("\nSummary of results:")
for name, (dist, t) in results.items():
    print(f"{name}: Distance = {dist:.2f}, Time = {t:.2f}s")
