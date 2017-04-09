#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 13:34:00 2017

@author: changlongjiang
"""

import graph
import Kmeans_rgb_modified
from queue import Queue

def max_flow(G, source, sink):
    augmented_paths = []
    max_flow = 0
    while True:
        flag, parent_map = bfs(G, source, sink)
        #print("parent_map",parent_map)
        #print(parent_map[-1])
        
        if not flag:
            break
        path=[]
        child = sink
        flow = 9223372036854775807
        while child != source:
            path.append(child)
            #print("path",path)
            father = parent_map[child]
            #print("flow_compare-v",G.find_edge_value(father,child))
            if flow > G.find_edge_value(father,child):
                flow = G.find_edge_value(father,child)
            child = father
            #print(flow)
        path.append(source)
        augmented_paths.append(path[::-1])
        #print(path,flow)
        G.update(path[::-1],flow)
        max_flow += flow
        print(max_flow)


    print("Augmented path")
    print(augmented_paths)
    return max_flow

def bfs(G,source,sink):
    visited_set = set()
    q = Queue()
    #print("visited",visited_set)
    parent_map = {}
    #print("parent_map",parent_map)
    current_adjcent=[]
    q.put(source)
    visited_set.add(source)
    flag = False
    flow = 9223372036854775807
    while not q.empty():
        current = q.get()
        #print("current",current)
        current_adjcent=G.find_adjcent(current)
        #print(current_adjcent)
        # print(current,"adjcent: ",current_adjcent)
        for i in range(len(current_adjcent)):
            if (G.find_edge_value(current,current_adjcent[i])>0) and (current_adjcent[i] not in visited_set):
                parent_map[current_adjcent[i]] = current 
                #print("parent_map",parent_map)
                visited_set.add(current_adjcent[i])
                #print("visited",visited_set)
                q.put(current_adjcent[i])
                #print("zzzz",current_adjcent[i])
                if current_adjcent[i] == sink:
                    flag = True
                    break;
        
    return flag, parent_map




if __name__=='__main__':
    m, n, likelihood_a, likelihood_b = Kmeans_rgb_modified.mainfunction()
    """
    m=5
    n=5
    likelihood_a=[0.3,0.4,0.5,0.6,0.7,
                          0.3,0.4,0.5,0.6,0.7,
                          0.3,0.4,0.5,0.6,0.7,
                          0.3,0.4,0.5,0.6,0.7,
                          0.3,0.4,0.5,0.6,0.7]
    likelihood_b=[0.3,0.4,0.5,0.6,0.7,
                                             0.3,0.4,0.5,0.6,0.7,
                                             0.3,0.4,0.5,0.6,0.7,
                                             0.3,0.4,0.5,0.6,0.7,
                                             0.3,0.4,0.5,0.6,0.7]
    """
    G=graph.Graph(m, n, likelihood_a, likelihood_b)
    print("zzzz",g.find_edge_value(1,-1))
    max_val = max_flow(G, 0, -1)
    print(max_val)

