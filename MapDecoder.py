import numpy
from PIL import Image

def img2Mat(imgPath):
	try:
		img = Image.open(imgPath)
	except:
		print("Sorry, this was not a valid image path.")
		return
	mat = numpy.array(img)
	print(mat)

if __name__ == "__main__":
	imgPath = raw_input("Path to desired map image: ")
	if len(imgPath) == 0:
		imgPath = "Images/1_color_river.png"
	img2Mat(imgPath)