import time

class N:
    def _init_(self,st=[[2,2,1,1,1,2,2],[2,2,1,1,1,2,2],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[2,2,1,1,1,2,2],[2,2,1,1,1,2,2]],prt=None,pCost=0):
        self.s=st
        self.p=prt
        self.a=None
        self.g=pCost

    def _lt_(self,o):
        return self.g<o.g

goal=[[2,2,0,0,0,2,2],[2,2,0,0,0,2,2],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,2,2],[2,2,0,0,0,2,2]]

def goalTest(s):
    return s==goal

total_exp=0

def succ(n):
    sc=[]
    dx2=[0,0,2,-2]
    dy2=[-2,2,0,0]
    dx1=[0,0,1,-1]
    dy1=[-1,1,0,0]
    for i in range(7):
        for j in range(7):
            if n.s[i][j]==1:
                for k in range(4):
                    c2i=i+dy2[k]
                    c2j=j+dx2[k]
                    c1i=i+dy1[k]
                    c1j=j+dx1[k]
                    if c2i<0 or c2i>=7 or c2j<0 or c2j>=7: continue
                    if n.s[c1i][c1j]==0: continue
                    if n.s[c2i][c2j]==0:
                        scpy=[r.copy() for r in n.s]
                        ch=N(scpy,n,n.g+1)
                        ch.s[c2i][c2j]=1
                        ch.s[c1i][c1j]=0
                        ch.s[i][j]=0
                        ch.a=[[i,j],[c2i,c2j]]
                        sc.append(ch)
                        global total_exp
                        total_exp+=1
    return sc

def disp(s):
    for r in s:
        print(r)

def bfs():
    sn=N()
    f=[]
    exp=[]
    f.append(sn)
    while True:
        if not f: return None
        cur=f.pop()
        disp(cur.s)
        print("Path cost:",cur.g)
        print()
        if cur.s in exp: continue
        if goalTest(cur.s):
            print("Search ended")
            print("Total nodes explored:",len(exp))
            return cur
        for ch in succ(cur):
            if ch.s not in exp:
                f.append(ch)
        exp.append(cur.s)

def actions(goal_n):
    a=[]
    while goal_n.p:
        a.append(goal_n.a)
        goal_n=goal_n.p
    a.reverse()
    return a

print("Search started")
start=time.time()
ans=bfs()
end=time.time()
print("Total nodes expanded:",total_exp)
print("Time taken:",end-start)
print()
disp(ans.s)
print()
print("Moves:")
mvs=actions(ans)
for mv in mvs:
    print(mv)
