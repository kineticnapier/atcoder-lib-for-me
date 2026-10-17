# AtCoder Python 総合ライブラリ

`competitive.py` をコピーして使う。添字は基本0始まり、区間は `[l,r)`。

| 分野 | 関数・クラス |
|---|---|
| 二分探索 | `lower_bound_int(lo, hi, pred)` |
| 累積和 | `prefix_sums(a)`, `range_sum(pref,l,r)` |
| 座標圧縮 | `coordinate_compress(a)` |
| いもす法 | `imos(n, updates)` |
| 尺取り法 | `two_pointer_count_ge(a,k)` （正整数列・k>0） |
| BFS/DFS | `bfs(g,s)`, `dfs_order(g,s)` |
| 2次元BFS | `grid_bfs(grid,(r,c))` |
| ダイクストラ | `dijkstra(g,s)` （辺は `(行先,重み)`） |
| Union-Find | `DSU(n)` |
| BIT | `Fenwick(n)` |
| セグ木 | `SegTree(a,op,e)` |
| トポロジカルソート | `topological_sort(g)` |

`heapq`, `bisect`, `accumulate`, `gcd`, `isqrt` もインポート済み。

## 使用例

```python
from competitive import *

# BFS
g = [[1], [0, 2], [1]]
print(bfs(g, 0))  # [0, 1, 2]

# セグ木（区間最大値）
s = SegTree([3, 1, 4, 1, 5], max, -INF)
print(s.prod(1, 4))  # 4

# Union-Find
d = DSU(4)
d.merge(0, 1)
print(d.same(0, 1))  # True
```

## DP・貪欲法について

DPや貪欲法は問題ごとに状態・遷移・選択基準が異なるため、単一の汎用関数にはしていない。

## コンテスト規則

生成AIを使って作成したコードについては、AtCoderの現行ルールを確認すること。コンテスト直前に作った本ファイルは、そのまま当日の提出で使えるとは限らない。
