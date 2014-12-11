import numpy as np
from numpy import linalg as la
import scipy as sp
import matplotlib.pyplot as plt
from sklearn.feature_extraction import image
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets

valid = False
while not valid:
	fileName = raw_input("Path to image: ")
	try:
		pic = sp.misc.imread(fileName, flatten=1)
		valid = True
	except:
		valid = False
		print "Sorry that is not a valid path.\n"

pic = pic.astype(int)
pic_x, pic_y, pic_z = np.atleast_3d(pic).shape
print "\nEnter the factor you want to downsample the picture by."
print "Note: make sure the factor is a power of two and works"
print "with the dimensions of the image provided.\n"

valid = False
while not valid:
	scaleNum = int(raw_input("Factor: "))
	#Check to see if power of two
	valid = scaleNum > 0 and ((scaleNum & (scaleNum - 1)) == 0)
	#Check to see if this works with pic provided
	valid = valid and (pic_x % scaleNum == 0) and (pic_y % scaleNum == 0)
	if not valid:
		print "That was not a valid factor."

timesToScale = int(np.log2(scaleNum))
for i in range(timesToScale):
	pic = pic[::2, ::2] + pic[1::2, ::2] + pic[::2, 1::2] + pic[1::2, 1::2]

picDimension = pic.shape[0]
newDimension = picDimension ** 2

#############Form the adjacency matrix###############################
eps = 1e6
def get_similarity(i_node, j_node):
	i_row = i_node // picDimension
	i_col = i_node % picDimension
	j_row = j_node // picDimension
	j_col = j_node % picDimension
	diff = pic[i_row][i_col] - pic[j_row][j_col]
	return np.exp((-diff ** 2)/(2 * eps ** 2))

print "W dimension: ", newDimension

W = [[0 for x in range(newDimension)] for x in range(newDimension)]
for m in range(newDimension):
	for n in range(newDimension):
		W[m][n] = get_similarity(m, n)

#############Form Degree Matrix#########################
D = [[0 for x in range(newDimension)] for x in range(newDimension)]
for m in range(newDimension):
	sum = 0
	for n in range(newDimension):
		sum += W[m][n]
	D[m][m] = sum


##############Finally find the normalized Laplacian#####################
Lsym = np.dot(W, np.sqrt(D))
#Compute D^-1/2 because does not work with power
for m in range(newDimension):
	D[m][m] = np.power(D[m][m], (-1/2))
Lsym = np.dot(D, Lsym)
Lsym = np.subtract(np.identity(newDimension), Lsym)
###############FIND EVECS#############################
valid = False
evals, evecs = la.eig(Lsym)
evec_matrix = []
while not valid:
	try:
		clusters = int(raw_input("Number of Clusters: "))
	except:
		print "Not valid number"
	if clusters <= 0:
		print "Not valid number"
	else:	
		clust_count = 0
		evec_matrix = []
		for vec in evecs:
			if clust_count == clusters:
				break
			else:	
				evec_matrix.append(vec)
				clust_count += 1
		if clust_count < clusters:
			print "Too many clusters"
		else:
			valid = True

evec_matrix = np.array(evec_matrix).T
print evec_matrix, "\n"

kmeans = KMeans(init='k-means++', n_clusters=clusters, n_init=10)
kmeans.fit(evec_matrix)

print evec_matrix

####################### K MEANS AND CLUSTERING ############################
kmeans = KMeans(n_clusters=clusters)
fig = plt.figure(1, figsize=(4, 3))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

plt.cla()
kmeans.fit(evec_matrix)
clusterLabelArray = kmeans.labels_
print clusterLabelArray
ax.scatter(evec_matrix[:, 3], evec_matrix[:, 0], evec_matrix[:, 2], c=clusterLabelArray.astype(np.float))
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
