from graph import *
import Kmeans_rgb_modified
from skimage.io import imread, imsave
import numpy as np

def dfs(capacity_graph):
    stack = []
    res = []
    stack.append(0)
    visited = {}
    stack_min = []
    while stack:
        cur = stack.pop()
        visited[cur] = 1
        if res:
            tmp_min = capacity_graph.find_edge_value(res[-1], cur)
            if not stack_min or tmp_min < stack_min[-1]:
                stack_min.append(tmp_min)
            else:
                stack_min.append(stack_min[-1])
        res.append(cur)
        if cur == -1:
            break
        flag = False
        cur_neighbor_list = capacity_graph.find_adjcent(cur)
        for i in cur_neighbor_list:
            if i not in visited:
                flag = True
                stack.append(i)
        while res and stack and (stack[-1] not in capacity_graph.find_adjcent(res[-1])):
            res.pop()
            stack_min.pop()
    return res, stack_min, visited

if __name__ == "__main__":
    #image, m, n, likelihood_a, likelihood_b = Kmeans_rgb_modified.mainfunction("cow.jpg")
    m = 2
    n = 2
    #likelihood_a = [0.1, 0.1, 0.1, 0.1, 0.1, 1, 1, 0.1, 0.1, 1, 1, 0.1, 0.1, 0.1, 0.1, 0.1]
    #likelihood_b = [1, 1, 1, 1, 1, 0.1, 0.1, 1, 1, 0.1, 0.1, 1, 1, 1, 1, 1]
    likelihood_a = [0.1, 0.1, 1, 1]
    likelihood_b = [1, 1, 0.1, 0.1]
    g = Graph(m, n, likelihood_a, likelihood_b, 0.2)
    res, stack_min, visited = dfs(g)
    total_flow = 0
    while len(res) != 1:
        total_flow += stack_min[-1]
        print(total_flow)
        g.update(res, stack_min[-1])
        res, stack_min, visited = dfs(g)
    cc = 0
'''
    one_side = np.zeros_like(image)
    for i in range(m):
        for j in range(n):
            if (i * n + j + 1) in visited:
                one_side[i][j] = image[i][j]
    imsave('foreground.jpg', one_side)
'''