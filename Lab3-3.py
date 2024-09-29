import random
import heapq

class N:
    def __init__(self, s=None, p=None, a=None, g=0, h=0):
        self.s = s if s else [[2, 2, 1, 1, 1, 2, 2], [2, 2, 1, 1, 1, 2, 2], [1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [2, 2, 1, 1, 1, 2, 2],
                               [2, 2, 1, 1, 1, 2, 2]]
        self.p = p
        self.a = a
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

goal = [[2, 2, 0, 0, 0, 2, 2], [2, 2, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 2, 2],
        [2, 2, 0, 0, 0, 2, 2]]

def is_goal(s):
    return s == goal

def h1(s):
    return sum(row.count(1) for row in s)

def h2(s):
    return sum(1 for i in range(7) for j in range(7) if s[i][j] == 1 and goal[i][j] == 0)

def fS(n):
    ans = []
    dm = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    mm = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for x in range(7):
        for y in range(7):
            if n.s[x][y] == 1:
                for d in range(4):
                    new_x, new_y = x + dm[d][0], y + dm[d][1]
                    mid_x, mid_y = x + mm[d][0], y + mm[d][1]
                    if 0 <= new_x < 7 and 0 <= new_y < 7 and n.s[mid_x][mid_y] == 1 and n.s[new_x][new_y] == 0:
                        new_s = [row[:] for row in n.s]
                        new_s[x][y] = 0
                        new_s[mid_x][mid_y] = 0
                        new_s[new_x][new_y] = 1
                        c = N(new_s, n, a=[(x, y), (new_x, new_y)], g=n.g + 1, h=h1(new_s))
                        ans.append(c)
    return ans

def a_star_search(h):
    start = N()
    frontier = []
    explored = set()

    start.h = h(start.s)
    heapq.heappush(frontier, start)

    while frontier:
        curr = heapq.heappop(frontier)

        if is_goal(curr.s):
            print("Search completed")
            return curr

        explored.add(str(curr.s))

        for child in fS(curr):
            if str(child.s) not in explored:
                child.h = h(child.s)
                heapq.heappush(frontier, child)

    return None

def extract_a(n):
    a = []
    while n.p is not None:
        a.append(n.a)
        n = n.p
    return a[::-1]

print("A* search started with h1")
res_n = a_star_search(h1)

if res_n:
    print("Total cost:", res_n.f)
    print("Moves:")
    for m in extract_a(res_n):
        print(m)

print("\nA* search started with h2")
res_n = a_star_search(h2)

if res_n:
    print("Total cost:", res_n.f)
    print("Moves:")
    for m in extract_a(res_n):
        print(m)
