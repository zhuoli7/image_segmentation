#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 13:34:00 2017
@author: Changlong Jiang / Yuxuan Mao / Zhuoli Peng / Hanjie Zhang
"""
import numpy as np
import Kmeans_rgb_modified
import bisect
import time

class Graph:
    def __init__(self,m,n,la,lb,penalty):
        self.size = m * n
        self.width = n
        self.length = m
        self.capacity = {0:{}, -1:{}}
        self.flow = {0:{}, -1:{}}
        self.height = [self.size + 2, 0]
        self.excess = [0]
        self.adj = {0:[], -1:[]}
        
        # initialization
        for i in range(self.size):
            j = i + 1
            self.flow[0].setdefault(j, la[i])
            self.flow[-1].setdefault(j, 0)
            self.height.append(0)
            self.excess.append(la[i])
            self.capacity[0].setdefault(j, la[i])
            self.capacity[-1].setdefault(j, 0)
            self.adj[0].append(j)
            self.adj[-1].append(j)
            
        self.excess.append(0)
        for i in range(self.size):
            j = i + 1
            xc = j // self.width
            yc = j % self.width
            self.adj.setdefault(j, [])
            self.adj[j].append(-1)
            self.adj[j].append(0)
            self.flow.setdefault(j, {})
            self.flow[j].setdefault(0, -la[i])
            self.flow[j].setdefault(-1, 0)
            self.capacity.setdefault(j, {})
            self.capacity[j].setdefault(0, 0)
            self.capacity[j].setdefault(-1, lb[i])
            if j > self.width:
                top = (xc - 1) * self.width + yc
                self.capacity[j].setdefault(top, penalty)
                self.flow[j].setdefault(top, 0)
                self.adj[j].append(top)
            if yc != 1:
                left = xc * self.width + yc - 1
                self.capacity[j].setdefault(left, penalty)
                self.flow[j].setdefault(left, 0)
                self.adj[j].append(left)
            if yc != 0:
                right = xc * self.width + yc + 1
                self.capacity[j].setdefault(right, penalty)
                self.flow[j].setdefault(right, 0)
                self.adj[j].append(right)
            if j <= self.size - self.width:
                bot = (xc + 1) * self.width + yc
                self.capacity[j].setdefault(bot, penalty)
                self.flow[j].setdefault(bot, 0)
                self.adj[j].append(bot)
    
    def push(self, start):
        if (self.height[start]>2*self.size-1):
                return False
        pushable = False
        v_has_excess = []
        for i in self.adj[start]:
            if(self.capacity[start][i]-self.flow[start][i]>0 and self.height[start]>self.height[i]):
                # if there is a pushable edge, set the flag to True
                pushable = True
                data_flow = min(self.excess[start], self.capacity[start][i]- self.flow[start][i])
                self.flow[start][i] += data_flow
                self.flow[i][start] = -self.flow[start][i]
                self.excess[start] -= data_flow
                if(self.excess[i]==0 and i!=-1 and i!=0):
                    v_has_excess.append([self.height[i], i, self.excess[i]])
                if(i!=0):
                    self.excess[i] += data_flow
        # if no flow is pushed, relabel
        if(not pushable):
            self.relabel(start)
        # if start point still has excess, return it as well
        if(self.excess[start]>0):
            v_has_excess.append([self.height[start], start, self.excess[start]])
        return v_has_excess

    def relabel(self, start):
        self.height[start]+=1

    def find_adjcent(self,x):
        return self.adj[x]

    def min_cut(self):
        foreground=[]
        background=[]
        for i in self.find_adjcent(0):
            if self.capacity[0][i] > self.flow[0][i]:
                foreground.append(i)
        for i in self.find_adjcent(-1):
            if self.capacity[i][-1] > self.flow[i][-1]:
                background.append(i)
        return foreground,background


if __name__=='__main__':
    start = time.time()
    image_d, m, n, likelihood_a, likelihood_b = Kmeans_rgb_modified.mainfunction()
    duration = time.time()-start
    print('Likelihood calculation done in: {0:.2f}s '.format(duration))
    g=Graph(m, n, likelihood_a, likelihood_b, 0.1)
    node_has_excess = []
    # push to a list
    start - time.time()
    for i in range(1, len(g.excess)-1):
        node_has_excess.append([g.height[i], i, g.excess[i]])
    # randomly pick a vertex
    while(node_has_excess):
        cur = node_has_excess.pop(-1)
        nodes = g.push(cur[1])
		# push nodes with excess to heap
        if(nodes):
            for i in nodes:
				# keep the list in sort by height
                bisect.insort(node_has_excess, i)
    foreground_list,background_list=g.min_cut()
    # set labels based on foreground
    duration = time.time()-start
    print('push-relabel done in: {0:.2f}s'.format(duration))
    start = time.time()
    labels = np.ones((m,n))
    for i in foreground_list:
        labels[((i-1)//n)][(i-1)%n]=0
    for i in background_list:
        labels[((i-1)//n)][(i-1)%n]=1
    Kmeans_rgb_modified.segementation_nf(image_d, labels)
    duration = time.time()-start
    print('segmentation done in: {0:.2f}'.format(duration))
    