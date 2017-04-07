from skimage.io import imread, imsave
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans
import time

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

if __name__=='__main__':
	start = time.time()
	fig = plt.figure()
	ax1 = fig.add_subplot(111, projection='3d')
	im = 'Cow1.jpeg'
	image = imread(im)
	centers, labels, temp = Km_cluster(image)
	duration = time.time()-start
	print('K-Means Cluster time is: {0:.2f}'.format(duration))
	# mplot(labels, temp)
	start = time.time()
	segementation(image, labels)
	duration = time.time()-start
	print('Segmentation time is: {0:.2f}'.format(duration))






