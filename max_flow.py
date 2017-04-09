#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 13:34:00 2017

@author: Changlong Jiang / Yuxuan Mao / Zhuoli Peng / Hanjie Zhang
"""
from queue import Queue
import numpy as np
from skimage.io import imread, imsave
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans
import time
import math
from skimage.measure import block_reduce
from sklearn.mixture import GaussianMixture
def KM_cluster(image):
    m, n, z = image.shape
    temp = image.reshape(m*n, z)
    result = KMeans(n_clusters = 2, n_jobs=-1)
    result.fit(temp)
    center = result.cluster_centers_
    labels = result.labels_
    return center, labels.reshape(m,n), temp, m, n

def mplot(centers, labels, temp):	
    x, y, z = [], [], []
    x1, y1, z1 = [], [], []
    o,p,q = centers[0]
    o1,p1,q1 = centers[1]	
    for i in range(len(temp)):
        if(labels[i] == 0):
            x.append(temp[i][0])
            y.append(temp[i][1])
            z.append(temp[i][2])
        else:
            x1.append(temp[i][0])
            y1.append(temp[i][1])
            z1.append(temp[i][2])
    ax1.scatter(x,y,z,c='b', marker='.', zorder = -1)
    ax1.scatter(x1,y1,z1, c='r',marker='.', zorder = -1)
    ax1.scatter(o, p, q, c = 'k', marker = 'o', s = 64, zorder = 10)
    ax1.scatter(o1, p1, q1, c = 'k', marker = 'o', s = 64, zorder = 10)
    ax1.set_xlabel('R')
    ax1.set_ylabel('G')
    ax1.set_zlabel('B')
    plt.show()

def segementation(image, labels):
    m, n, z = image.shape
    one_side = np.zeros_like(image)
    another_side = np.zeros_like(image)
    for i in range(m):
        for j in range(n):
            if(labels[i][j] == 0):
                one_side[i][j] = image[i][j]
            else:
                another_side[i][j] = image[i][j]
    imsave('one.jpg', one_side)
    imsave('two.jpg', another_side)

def segementation_nf(image, labels):
    m, n, z = image.shape
    one_side = np.zeros_like(image)
    another_side = np.zeros_like(image)
    for i in range(m):
        for j in range(n):
            if(labels[i][j] == 0):
                one_side[i][j] = image[i][j]
            else:
                another_side[i][j] = image[i][j]
    imsave('one_nf.jpg', one_side)
    imsave('two_nf.jpg', another_side)

def downsample(image,down_rate):
    image_d = block_reduce(image, block_size=(down_rate, down_rate, 1), func=np.max)
    return image_d
	
def Euclidian_distance(matrix, centers):
    mat_a = matrix - centers[0]
    mat_b = matrix - centers[1]
    dist_a = np.sum(mat_a**2,axis=1)**0.5
    dist_b = np.sum(mat_b**2,axis=1)**0.5
    return dist_a, dist_b

def regularization(matrix):
    max_value = np.max(matrix)
    min_value = np.min(matrix)
    matrix_reged = (matrix - min_value)/(max_value - min_value)
    mat_reg = 1/(1+math.e**matrix_reged)
    return mat_reg

def GMM(image):
    m, n, z = image.shape	
    temp = image.reshape(m*n, z)
    result_GMM = GaussianMixture(n_components = 2).fit(image)
    means = result_GMM.means_
    covariances = result_GMM.covariances_

def mainfunction():
    start = time.time()
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    im = 'WechatIMG128.jpeg'
    image = imread(im)
    image_d = downsample(image,4)	
    centers, labels, temp, m, n = KM_cluster(image_d)
    duration = time.time()-start
    # print('K-Means Cluster time is: {0:.2f}s'.format(duration))
    # mplot(centers, labels, temp)
    start = time.time()
    # segementation(image_d, labels)
    duration = time.time()-start
    # print('Segmentation time is: {0:.2f}s'.format(duration))

    #########
    dist_a, dist_b = Euclidian_distance(temp, centers)
    likelihood_a = regularization(dist_a)
    likelihood_b = regularization(dist_b)

    # print('likelihood_a',likelihood_a)
    # print('likelihood_b',likelihood_b)
    
    ## creat label with likelihood fro segmentation
    ## only for test, not needed for the final segmentation
    #label_lik = likelihood_a - likelihood_b
    #label_lik[label_lik >= 0] = 0
    #label_lik[label_lik < 0] = 1
    #segementation(image_d, label_lik.reshape(m,n))
    return image_d, m, n, likelihood_a, likelihood_b

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
            penalty = 0.2
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
    for i in G.find_adjcent(1):
        print(G.find_edge_value(1,i))
    for i in G.find_adjcent(0):
        print(G.find_edge_value(0,i))
        if G.find_edge_value(0,i) > 0:
            foreground.append(i)
    for i in G.find_adjcent(-1):
        print(G.find_edge_value(i,-1))
        if G.find_edge_value(i,-1) > 0:
            background.append(i)    
    #print(foreground)
    #print(background)
    print(augmented_paths)
    return max_flow, foreground, background

def bfs(G,source,sink):
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
    image_d, m, n, likelihood_a, likelihood_b = mainfunction()
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
        labels[(i//n)][(i%n)-1]=0
    for i in background_list:
        labels[(i//n)][(i%n)-1]=1

    segementation_nf(image_d, labels)
    print(max_flow_final)

