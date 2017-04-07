# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from skimage.io import imread, imsave
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans
from colorsys import rgb_to_hls
import time

def convert_to_hls(image):
    m, n, z = image.shape
    hls_image = np.zeros([m,n,z])
    ls_value = np.zeros([m,n,2])
    for i in range(m):
        for j in range(n):
            hls_image[i][j] = rgb_to_hls(image[i][j][0]/255,
                                  image[i][j][1]/255, image[i][j][2]/255)
            ls_value[i][j][0] = hls_image[i][j][1]
            ls_value[i][j][1] = hls_image[i][j][2]
    return hls_image, ls_value

def KMeans_cluster(satuarion):
    m, n, z = satuarion.shape
    temp = satuarion.reshape(m*n, z)
    result = KMeans(n_clusters=2, n_jobs=-1)
    result.fit(temp)
    centers = result.cluster_centers_
    labels = result.labels_
    return centers, labels.reshape(m,n), temp

def segmentation(image, labels):
    one_side = np.zeros_like(image)
    another_side = np.zeros_like(image)
    m, n = labels.shape
    for i in range(m):
        for j in range(n):
            if(labels[i][j] == 0):
                one_side[i][j] = image[i][j]
            else:
                another_side[i][j] = image[i][j]
    imsave('satuarion_a.jpg', one_side)
    imsave('saturation_b.jpg', another_side)

if __name__=='__main__':
    start = time.time()
    fig = plt.figure()
    aax1 = fig.add_subplot(111, projection='3d')
    im = 'Beijing2.jpg'
    image = imread(im)
    new_image, saturation = convert_to_hls(image)
    centers, labels, temp = KMeans_cluster(saturation)
    duration = time.time()-start
    print('K-Means Cluster time is: {0:.2f}s'.format(duration))
    # mplot(centers, labels, temp)
    start = time.time()
    segmentation(image, labels)
    duration = time.time()-start
    print('Segmentation time is: {0:.2f}s'.format(duration))