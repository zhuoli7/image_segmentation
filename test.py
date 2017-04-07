from skimage.io import imread, imsave
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans
import time
import math
from skimage.measure import block_reduce
from sklearn.mixture import GaussianMixture

def Km_cluster(image):
	m, n, z = image.shape
	temp = image.reshape(m*n, z)
	result = KMeans(n_clusters = 2)
	result.fit(temp)
	center = result.cluster_centers_
	labels = result.labels_
	return center, labels, temp

def mplot(labels, temp):	
	x, y, z = [], [], []
	x1, y1, z1 = [], [], []
	for i in range(len(temp)):
		if(labels[i] == 0):
			x.append(temp[i][0])
			y.append(temp[i][1])
			z.append(temp[i][2])
		else:
			x1.append(temp[i][0])
			y1.append(temp[i][1])
			z1.append(temp[i][2])
	ax1.scatter(x,y,z,c='r', marker='o')
	ax1.scatter(x1,y1,z1, c='g',marker='*')
	plt.show()

def segementation(image, labels):
	one_side = np.empty_like(image)
	another_side = np.empty_like(image)
	m, n, z = image.shape
	new = labels.reshape(m, n)
	for i in range(m):
		for j in range(n):
			if(new[i][j] == 0):
				one_side[i][j] = image[i][j]
				another_side[i][j] = np.array([0,0,0])
			else:
				another_side[i][j] = image[i][j]
				one_side[i][j] = np.array([0,0,0])
	imsave('one.jpeg', one_side)
	imsave('two.jpeg', another_side)

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


if __name__=='__main__':
	start = time.time()
	fig = plt.figure()
	ax1 = fig.add_subplot(111, projection = '3d')
	im = 'IMAG0428.jpg'
	image = imread(im)
	image_d = downsample(image,1)
	centers, labels, temp = Km_cluster(image_d)
	duration = time.time()-start
	print('K-Means Cluster time is: {0:.2f}'.format(duration))
	# mplot(labels, temp)
	start = time.time()
	# segementation(image, labels)
	duration = time.time()-start
	print('Segmentation time is: {0:.2f}'.format(duration))

	dist_a, dist_b = Euclidian_distance(temp, centers)
	likelihood_a = regularization(dist_a)
	likelihood_b = regularization(dist_b)

	# print(likelihood_a)
	# print(likelihood_b)

	# creat label with likelihood fro segmentation
	label_lik = likelihood_a - likelihood_b
	label_lik[label_lik >= 0] = 0
	label_lik[label_lik < 0] = 1
	segementation(image, label_lik)

