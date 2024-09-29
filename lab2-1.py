from collections import deque

class Node:
    def _init_(self,state,parent=None):
        self.state=state
        self.parent=parent

def successors(node):
    succ=[]
    idx=node.state.index(0)
    moves=[-1,1,3,-3]
    for move in moves:
        im=idx+move
        if im>=0 and im<9:
            ns=list(node.state)
            temp=ns[im]
            ns[im]=ns[idx]
            ns[idx]=temp
            succ.append(Node(ns,node))
    return succ

def bfs(start,goal):
    start_node=Node(start)
    goal_node=Node(goal)
    q=deque([start_node])
    visited=set()
    explored=0
    while q:
        node=q.popleft()
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        print(node.state)
        explored+=1
        if node.state==list(goal_node.state):
            path=[]
            while node:
                path.append(node.state)
                node=node.parent
            print('Total nodes explored',explored)
            return path[::-1]
        for succ in successors(node):
            q.append(succ)
    print('Total nodes explored',explored)
    return None

start_state=[1,2,3,4,5,6,7,8,0]
goal_state=[1,2,3,4,5,6,0,7,8]

sol=bfs(start_state,goal_state)
if sol:
    print("Solution found:")
    for step in sol:
        print(step)
else:
    print("No solution found.")
