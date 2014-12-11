import time
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from sklearn.feature_extraction import image
from sklearn.cluster import spectral_clustering

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
print "\nEnter the sample you want to downsample the picture by."
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
 
graph = image.img_to_graph(pic)
beta = 5
eps = 1e-6
#Not too sure what this means yet
graph.data = np.exp(-beta * graph.data / pic.std()) + eps
print ""

valid = False
while not valid:
	N_REGIONS = int(raw_input("Amount of clusters: "))
	if N_REGIONS <= 1:
		print "Invalid cluster number."
	else:
		valid = True
 
print "Working..."

startTime = time.time()
labels = spectral_clustering(graph, n_clusters=N_REGIONS,
                             random_state=1)
finishTime = time.time()
labels = labels.reshape(pic.shape)
plt.figure(figsize=(5, 5))
plt.imshow(pic,   cmap=plt.cm.gray)
for l in range(N_REGIONS):
    plt.contour(labels == l, contours=1,
                colors=[plt.cm.spectral(l / float(N_REGIONS)), ])
plt.xticks(())
plt.yticks(())
plt.title('Downsampling: %d, Clusters %d, Total Time: %f.2' % (scaleNum, N_REGIONS, (finishTime - startTime)))
plt.show()