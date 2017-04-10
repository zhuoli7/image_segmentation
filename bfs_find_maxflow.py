#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 13:34:00 2017
@author: Changlong Jiang / Yuxuan Mao / Zhuoli Peng / Hanjie Zhang
"""
from queue import Queue
import numpy as np
import Kmeans_rgb_modified

class Graph:
    def __init__(self,m,n,la,lb):
        self.size = m * n
        self.width = n
        self.length = m
        self.edg = {0:{},-1:{}}
        self.adj = {0:[],-1:[]}
        self.res = {-1:{}}
        for i in range(self.size):
            # source to every node
            self.edg[0].setdefault(i+1, la[i])
            # source's adjcent node
            self.adj[0].append(i+1)
            self.adj[-1].append(i+1)
            self.edg[-1].setdefault(i+1, 0)
            
        for i in range(self.size):
            xc = i // self.width
            yc = (i + 1) % self.width
            self.edg.setdefault(i + 1, {})
            # set penalty
            penalty = 0.07
            # current node to sink
            self.edg[i + 1].setdefault(0, 0)
            self.edg[i + 1].setdefault(-1, lb[i])
            self.adj.setdefault(i + 1, [])
            self.adj[i + 1].append(-1)
            # current node to adjcent node
            if xc != 0:
                if yc == 0:
                    yct = self.width
                else:
                    yct = yc
                top = (xc - 1) * self.width + yct
                self.edg[i + 1].setdefault(top, penalty)
                self.adj[i + 1].append(top)
            if yc != 1:
                if yc == 0:
                    yct = self.width
                else:
                    yct = yc
                left = xc * self.width + yct - 1
                self.edg[i + 1].setdefault(left, penalty)
                self.adj[i + 1].append(left)
            if yc != 0:
                right = xc * self.width + yc + 1
                self.edg[i + 1].setdefault(right, penalty)
                self.adj[i + 1].append(right)
            if xc != self.length - 1:
                if yc == 0:
                    xct = xc + 1
                else:
                	xct = xc
                bot = (xct + 1) * self.width + yc
                self.edg[i + 1].setdefault(bot, penalty)
                self.adj[i + 1].append(bot)

    def find_adjcent(self,x):
        return self.adj[x]

    def update(self,path,min):
        l=len(path)
        for i in range(l):
            if(i + 1 < l):
                self.edg[path[i]][path[i + 1]] = self.edg[path[i]][path[i + 1]] - min
                self.edg[path[i + 1]][path[i]] = self.edg[path[i + 1]][path[i]] + min

    def find_edge_value(self,start,end):
        return self.edg[start][end]
    
def f_f(G, source, sink):
    augmented_paths = []
    foreground=[]
    background=[]
    max_flow = 0
    while True:
        flag, parent_map = find_valid_path(G, source, sink)
        #print("parent_map",parent_map)
        #print(parent_map[-1])
        if flag != True:
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
        
    #print(foreground)
    #print(background)
    print(augmented_paths)
    for i in G.find_adjcent(0):
        #print(G.find_edge_value(0,i))
        if G.find_edge_value(0,i) > 0:
            foreground.append(i)
    for i in G.find_adjcent(-1):
        #print(G.find_edge_value(i,-1))
        if G.find_edge_value(i,-1) > 0:
            background.append(i)
    return max_flow, foreground, background

def find_valid_path(G,source,sink):
    q = Queue()
    parent_map = {}
    current_adjcent=[]
    visited_set = []
    #print("visited",visited_set)
    #print("parent_map",parent_map)
    q.put(source)
    visited_set.append(source)
    flag = False
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
                visited_set.append(current_adjcent[i])
                #print("visited",visited_set)
                q.put(current_adjcent[i])
                #print("zzzz",current_adjcent[i])
                if current_adjcent[i] == sink:
                    flag = True
                    break;
        
    return flag, parent_map




if __name__=='__main__':
    image_d, m, n, likelihood_a, likelihood_b = Kmeans_rgb_modified.mainfunction("cow.jpg")
    g=Graph(m, n, likelihood_a, likelihood_b)
    #print(g.find_adjcent(-1))
    #print(g.find_edge_value(1,-1))
    #print(g.find_edge_value(5,165))
    #print(g.find_edge_value(165,-1))
    #g.update([0,5,165,-1],0.2)
    #print(g.find_edge_value(0,5))
    #print(g.find_edge_value(5,165))
    #print(g.find_edge_value(165,-1)
    #g=Graph(m, n, likelihood_a, likelihood_b)
    max_flow_final,foreground_list, background_list= f_f(g, 0, -1)
    labels=np.ones((m,n))
    for i in foreground_list:
        labels[((i-1)//n)][(i-1)%n]=0
    for i in background_list:
        labels[((i-1)//n)][(i-1)%n]=1

    Kmeans_rgb_modified.segementation_nf(image_d, labels)
    print(max_flow_final)
