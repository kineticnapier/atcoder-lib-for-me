"""Competitive programming helpers (Python 3.11+). Indices are 0-based."""
from collections import deque
from bisect import bisect_left, bisect_right
from heapq import heappush, heappop
from itertools import accumulate
from math import gcd, isqrt

INF = 10**30

def lower_bound_int(lo, hi, pred):
    """First x in [lo, hi) satisfying monotone False->True pred; hi if none."""
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid): hi = mid
        else: lo = mid + 1
    return lo

def prefix_sums(a):
    return [0] + list(accumulate(a))

def range_sum(pref, l, r):
    """Sum of a[l:r]."""
    return pref[r] - pref[l]

def coordinate_compress(a):
    vals = sorted(set(a))
    rank = {x:i for i,x in enumerate(vals)}
    return [rank[x] for x in a], vals

def imos(n, updates):
    """updates: iterable of (l,r,value), applying to [l,r)."""
    diff = [0] * (n + 1)
    for l,r,v in updates:
        diff[l] += v
        diff[r] -= v
    return list(accumulate(diff))[:n]

def two_pointer_count_ge(a, k):
    """Count subarrays with sum >= k, assuming positive a and k > 0."""
    n = len(a); r = 0; s = 0; ans = 0
    for l in range(n):
        while r < n and s < k:
            s += a[r]; r += 1
        if s >= k: ans += n - r + 1
        if r == l:
            r += 1
        else:
            s -= a[l]
    return ans

def bfs(graph, start):
    dist = [-1] * len(graph)
    dist[start] = 0
    q = deque([start])
    while q:
        v = q.popleft()
        for u in graph[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist

def dfs_order(graph, start):
    """Iterative DFS visit order."""
    seen = [False] * len(graph); seen[start] = True
    stack = [start]; order = []
    while stack:
        v = stack.pop(); order.append(v)
        for u in reversed(graph[v]):
            if not seen[u]:
                seen[u] = True; stack.append(u)
    return order

def grid_bfs(grid, start, wall='#'):
    """Grid of strings; coordinates (row,column)."""
    h = len(grid); w = len(grid[0]); sr,sc = start
    dist = [[-1]*w for _ in range(h)]
    if grid[sr][sc] == wall: return dist
    dist[sr][sc] = 0; q = deque([(sr,sc)])
    for_pop = q.popleft
    while q:
        r,c = for_pop()
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr,nc = r+dr,c+dc
            if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] != wall and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr,nc))
    return dist

def dijkstra(graph, start):
    """graph[v] contains (neighbor, nonnegative_weight)."""
    dist = [INF]*len(graph); dist[start] = 0
    pq = [(0,start)]
    while pq:
        d,v = heappop(pq)
        if d != dist[v]: continue
        for u,w in graph[v]:
            nd = d+w
            if nd < dist[u]:
                dist[u] = nd; heappush(pq,(nd,u))
    return dist

class DSU:
    def __init__(self,n):
        self.p = [-1]*n
    def leader(self,a):
        while self.p[a] >= 0:
            if self.p[self.p[a]] >= 0: self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a
    def merge(self,a,b):
        a,b = self.leader(a),self.leader(b)
        if a == b: return False
        if -self.p[a] < -self.p[b]: a,b = b,a
        self.p[a] += self.p[b]; self.p[b] = a
        return True
    def same(self,a,b): return self.leader(a) == self.leader(b)
    def size(self,a): return -self.p[self.leader(a)]

class Fenwick:
    """Point add, prefix/range sum; 0-indexed API."""
    def __init__(self,n): self.n=n; self.bit=[0]*(n+1)
    def add(self,i,x):
        i += 1
        while i <= self.n:
            self.bit[i] += x; i += i & -i
    def prefix(self,r):
        s = 0
        while r:
            s += self.bit[r]; r -= r & -r
        return s
    def sum(self,l,r): return self.prefix(r)-self.prefix(l)

class SegTree:
    """Monoid segment tree; prod(l,r) uses [l,r)."""
    def __init__(self,a,op,e):
        self.n=len(a); self.op=op; self.e=e; self.size=1
        while self.size < self.n: self.size *= 2
        self.d=[e]*(2*self.size)
        self.d[self.size:self.size+self.n] = a
        for i in range(self.size-1,0,-1): self.d[i]=op(self.d[2*i],self.d[2*i+1])
    def set(self,p,x):
        p+=self.size; self.d[p]=x
        while p>1:
            p//=2; self.d[p]=self.op(self.d[2*p],self.d[2*p+1])
    def get(self,p): return self.d[self.size+p]
    def prod(self,l,r):
        vl=vr=self.e; l+=self.size; r+=self.size
        while l<r:
            if l&1: vl=self.op(vl,self.d[l]); l+=1
            if r&1: r-=1; vr=self.op(self.d[r],vr)
            l//=2; r//=2
        return self.op(vl,vr)

def topological_sort(graph):
    n=len(graph); indeg=[0]*n
    for adj in graph:
        for u in adj: indeg[u]+=1
    q=deque(i for i,d in enumerate(indeg) if d==0); order=[]
    while q:
        v=q.popleft(); order.append(v)
        for u in graph[v]:
            indeg[u]-=1
            if indeg[u]==0: q.append(u)
    return order if len(order)==n else None
