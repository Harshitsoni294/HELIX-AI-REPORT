from collections import deque
import time

def valid(s):
    m,c,b=s
    if m<0 or c<0 or m>3 or c>3:
        return False
    if m>0 and m<c:
        return False
    if 3-m>0 and 3-m<3-c:
        return False
    return True

def successors(s):
    succ=[]
    m,c,b=s
    moves=[(2,0),(0,2),(1,1),(1,0),(0,1)]
    for move in moves:
        if b==1:
            ns=(m-move[0],c-move[1],0)
        else:
            ns=(m+move[0],c+move[1],1)
        if valid(ns):
            succ.append(ns)
    return succ

def dfs(start,goal):
    stk=[(start,[])]
    visited=set()
    while stk:
        state,path=stk.pop()
        if state in visited:
            continue
        visited.add(state)
        path=path+[state]
        if state==goal:
            return path
        for succ in successors(state):
            stk.append((succ,path))
    return None

start=(3,3,1)
goal=(0,0,0)

begin_dfs=time.time()

sol_dfs=dfs(start,goal)
if sol_dfs:
    print("\nDFS Solution:")
    for step in sol_dfs:
        print(step)
else:
    print("No DFS solution.")

end_dfs=time.time()

print(f"Total DFS runtime:{end_dfs-begin_dfs}")
