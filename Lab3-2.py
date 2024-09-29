import time
import heapq

class N:
    def _init_(self, st=None, p=None, a=None, g=0, h=0):
        self.s = st if st else [[2, 2, 1, 1, 1, 2, 2], [2, 2, 1, 1, 1, 2, 2], [1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [2, 2, 1, 1, 1, 2, 2],
                                [2, 2, 1, 1, 1, 2, 2]]
        self.p = p
        self.a = a
        self.g = g  
        self.h = h  
        self.f = g + h  

    def _lt_(self, o):
        return self.f < o.f  

goal = [[2, 2, 0, 0, 0, 2, 2], [2, 2, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 0, 2, 2],
        [2, 2, 0, 0, 0, 2, 2]]

def goal_test(s):
    return s == goal

def h1(s):
    return sum(r.count(1) for r in s)

def h2(s):
    return sum(1 for i in range(7) for j in range(7) if s[i][j] == 1 and goal[i][j] == 0)

def succ(n):
    sc = []
    dm = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    mm = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for x in range(7):
        for y in range(7):
            if n.s[x][y] == 1:
                for d in range(4):
                    nx, ny = x + dm[d][0], y + dm[d][1]
                    mx, my = x + mm[d][0], y + mm[d][1]

                    if 0 <= nx < 7 and 0 <= ny < 7 and n.s[mx][my] == 1 and n.s[nx][ny] == 0:
                        ns = [r[:] for r in n.s]
                        ns[x][y] = 0
                        ns[mx][my] = 0
                        ns[nx][ny] = 1
                        ch = N(ns, n, a=[(x, y), (nx, ny)], g=n.g + 1, h=h1(ns))
                        sc.append(ch)
    return sc

def astar(h):
    init_n = N()
    f = []
    exp = set()

    init_n.h = h(init_n.s)
    heapq.heappush(f, init_n)

    while f:
        cur = heapq.heappop(f)

        if goal_test(cur.s):
            print("Search completed")
            return cur

        exp.add(str(cur.s))

        for ch in succ(cur):
            if str(ch.s) not in exp:
                ch.h = h(ch.s)
                heapq.heappush(f, ch)

    return None

def actions(n):
    a = []
    while n.p:
        a.append(n.a)
        n = n.p
    return a[::-1]

print("A* search started with heuristic one")
start = time.time()
res = astar(h1)
end = time.time()

if res:
    print("Total cost:", res.f)
    print("Elapsed time:", end - start)
    print("Moves:")
    for mv in actions(res):
        print(mv)
else:
    print("No solution found.")

print("\nA* search started with heuristic two")
start = time.time()
res = astar(h2)
end = time.time()

if res:
    print("Total cost:", res.f)
    print("Elapsed time:", end - start)
    print("Moves:")
    for mv in actions(res):
        print(mv)
else:
    print("No solution found.")
