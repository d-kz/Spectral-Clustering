import numpy
from PIL import Image

def img2Mat(imgPath):
	img = Image.open(imgPath)
	mat = numpy.array(img)
	print(mat)

if __name__ == "__main__":
	imgPath = raw_input("Path to desired map image: ")
	if len(imgPath) == 0:
		imgPath = "Images/1_color_river.png"
	img2Mat(imgPath)