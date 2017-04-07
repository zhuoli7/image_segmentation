#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 00:04:49 2017

@author: changlongjiang
"""

from queue import Queue
"""
class Node:
	def __init__(self, x, y, val):
		self.x = x
		self.y = y
		self.val = val
	def coordinates(self):
		return (self.x, self.y)	
	def val(self):
		return val
"""
class Edge:
    def __init__(self, node1, node2, capacity):
        self.begin = node1
        self.end = node2
        self.capacity = capacity
        self.residual_capacity = 0
    
    def __repr__(self):
        return "%s -> %s : residual : %d / left: %d" % (self.begin, self.end, self.residual_capacity, self.capacity)
class Graph:
    def __init__(self):
        
        self.edges = []
        self.argument_path=[]
        self.max_flow = 0
    def initial_edge(self, node1, node2, capacity):
        new = Edge(node1, node2, capacity)
        self.edges.append(new)
    def Find_Argument_Path(self,s,t):
        visited_set=set()
        q=Queue()
        parent_map = {}
        q.put(s)
        print(self.edges[0])
        visited_set.add(s)
        print(visited_set)
        flag = False
        bottle_neck=10000
        while q.empty()!=True:
            current = q.get()
            for i in range(len(self.edges)):
                if (self.edges[i].begin == current) and (self.edges[i].end not in visited_set) and (self.edges[i].capacity > 0):
                    parent_map[self.edges[i].begin]=self.edges[i].end
                    print(parent_map)
                    if bottle_neck > self.edges[i].capacity:
                        bottle_neck = self.edges[i].capacity
                    
                    q.put(self.edges[i].end)
                    visited_set.add(self.edges[i].end)
                    self.edges[i].capacity -= bottle_neck
                    self.edges[i].residual_capacity += bottle_neck
                    if self.edges[i].end == t:
                        flag = True
                        self.max_flow += bottle_neck
                        break;
        self.argument_path.append(parent_map)

        print(parent_map)
        return flag
    
            
    

f=open("hw5test.txt")
A=Graph()


for lines in f:
    # print(lines)
    a=lines.split(' ')
    print(a[0],a[1])
    A.initial_edge('s',a[0],1)
    A.initial_edge(a[0],a[1],1)
    
    A.initial_edge(a[1],'t',1)
 
while A.Find_Argument_Path('s','t')== True:
    continue
print(A.max_flow)  