#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 13:34:00 2017
@author: Changlong Jiang / Yuxuan Mao / Zhuoli Peng / Hanjie Zhang
"""
import numpy as np
import Kmeans_rgb_modified
import bisect
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
        #print("In push function *** current height",self.height[start],"source height", self.height[0])

        if (self.height[start]>2*self.size-1):
                return False
        pushable = False
        v_has_excess = []
        #print("v_has_excess_list:",v_has_excess)
        for i in self.adj[start]:
            #print("verdex:",start,i)
            #print("condition1:",self.capacity[start][i],self.flow[start][i])
            #print("condition2:",self.height[start],self.height[i])
            if(self.capacity[start][i]-self.flow[start][i]>0 and self.height[start]>self.height[i]):
                # if there is a pushable edge, set the flag to True
                #print("inininin!!")
                pushable = True
                data_flow = min(self.excess[start], self.capacity[start][i]- self.flow[start][i])
                #print("data_flow",data_flow)
                #print("befor +, flow[start][i]",start,i,self.flow[start][i])
                self.flow[start][i] += data_flow
                #print("after +, flow[start][i]",start,i,self.flow[start][i])
                self.flow[i][start] = -self.flow[start][i]
                #print("before excess[",i,"]",self.excess[i])
                self.excess[start] -= data_flow
                if(self.excess[i] == 0 and i != -1 and  i!=0):
                    v_has_excess.append([self.height[i], i, self.excess[i]])
                if(i!=0):
                    self.excess[i] += data_flow
                #print("after excess[",i,"]",self.excess[i])
        # if no flow is pushed, relabel and push again
        #print("after push ",start)
        #print("capacity:",g.capacity)
        #print("flow:",g.flow)
        #print("adj:", g.adj)
        #print("excess:", g.excess)
        #print("height:", g.height)
        if(not pushable):
            self.relabel(start)

            # if start point still has excess, return it as well
            #print(self.excess[start])
        if(self.excess[start]>0):
            v_has_excess.append([self.height[start], start, self.excess[start]])
        #print('v_has_excess',v_has_excess)
        return v_has_excess

    def relabel(self, start):
        self.height[start]+=1
        #print("height[",start,"]", self.height[start])

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
    #image_d, m, n, likelihood_a, likelihood_b = Kmeans_rgb_modified.mainfunction()

    m=2
    n=2
    likelihood_a=[0.1,0.2,0.7,0.9]
    likelihood_b=[0.9,0.8,0.3,0.1]
    
    g=Graph(m, n, likelihood_a, likelihood_b, 0.1)
    """
    print("original capacity:",g.capacity)
    print("original flow:",g.flow)
    print("original adj:", g.adj)
    print("original excess:", g.excess)
    print("original height:", g.height)
    """
    node_has_excess = []
    # push to heap
    for i in range(1, len(g.excess)-1):
        node_has_excess.append([g.height[i], i, g.excess[i]])
    #print('origin node_has_excess_list',node_has_excess)
    # randomly pick a vertex
    while(node_has_excess):
        #print("node_has_excess:",node_has_excess)
        cur = node_has_excess.pop(-1)
        
        nodes = g.push(cur[1])
		# push nodes with excess to heap
		# print('node:', nodes)
        if(nodes):
            for n in nodes:
				# keep the list in sort by height
				# print('before',heap)
                bisect.insort(node_has_excess, n)
				# print('after',heap)
    foreground_list,background_list=g.min_cut()
    print(foreground_list,background_list)
    """
    labels=np.ones((m,n))
    for i in foreground_list:
        labels[((i-1)//n)][(i-1)%n]=0
    for i in background_list:
        labels[((i-1)//n)][(i-1)%n]=1

    Kmeans_rgb_modified.segementation_nf(image_d, labels)
    
    """
    