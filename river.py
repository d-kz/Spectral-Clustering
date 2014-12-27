from scipy import ndimage
from skimage import color
import os

directory = os.path.dirname(os.path.realpath(__file__))
# the directory from which river.py is executed

brazil = ndimage.imread(directory + "/Images/ASA-IMP-brazil3_H1.jpg")
brazil = color.rgb2hsv(brazil)
print(repr(brazil))
