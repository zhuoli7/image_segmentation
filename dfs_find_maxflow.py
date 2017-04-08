from graph import *

def dfs(capacity_graph):
    stack = []
    res = []
    stack.append(0)
    visited = {}
    stack_min = []
    while stack:
        cur = stack.pop()
        if res:
            tmp_min = min(capacity_graph.find_edge_value(cur, res[-1]), capacity_graph.find_edge_value(res[-1], cur))
            if not stack_min or tmp_min < stack_min[-1]:
                stack_min.append(tmp_min)
            else:
                stack_min.append(stack_min[-1])
        res.append(cur)
        if cur == -1:
            break
        cur_neighbor_list = capacity_graph.find_adjcent(cur)
        if not cur_neighbor_list:
            res.pop()
            stack_min.pop()
            continue
        for i in cur_neighbor_list:
            if i not in visited:
                stack.append(i)
                visited[i] = 1
    return res, stack_min, visited

if __name__ == "__main__":
    import Kmeans_rgb_modified
    from skimage.io import imread, imsave
    import numpy as np

    m, n, likelihood_a, likelihood_b = Kmeans_rgb_modified.mainfunction()
    G = Graph(m, n, likelihood_a, likelihood_b)
    res, stack_min, visisted = dfs(G)
    while res:
        G.update(res, stack_min[-1])
        res, stack_min, visisted = dfs(G)
    cc = 0
    