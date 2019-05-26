import closeststore as cs


adj = [
#список смежности
    [1, 3],  # 0
    [0, 3, 4, 5],  # 1
    [4, 5],  # 2
    [0, 1, 5],  # 3
    [1, 2],  # 4
    [1, 2, 3]  # 5
]

level = [-1] * len(adj)


def bfs(s):
    global level
    level[s] = 0
    queue = [s]
    while queue:
        v = queue.pop(0)
        for w in adj[v]:
            if level[w] is -1:
                queue.append(w)
                level[w] = level[v] + 1


for i in range(len(adj)):
    if level[i] is -1:
        bfs(i)

print(level[2])