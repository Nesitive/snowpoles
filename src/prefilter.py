import colorsys
from multiprocessing import Process, Value
import os
from pathlib import Path
from PIL import Image

def apply_filter(imagefile, image):
	for y in range(imagefile.height):
		for x in range(imagefile.width):
			pixel = list(colorsys.rgb_to_hsv(*image[x, y]))
			if (pixel[0] < 0.958 and pixel[0] > 0.042):
				image[x, y] = (0, 0, 0)
				continue
			pixel[1] = 1
			pixel[2] = 255
			rgb = colorsys.hsv_to_rgb(*pixel)
			image[x, y] = (round(rgb[0]), round(rgb[1]), round(rgb[2]))
	return image

def filter_list(imagepaths, progress):
	global total
	for file in imagepaths:
		imagefile = Image.open(file)
		image = imagefile.load()
		apply_filter(imagefile, image)
		outfile = str(file).replace("\\", "/").split("/")
		outfile[1] = "Snow Station Photos 2023-2024 Filtered"
		if not os.path.exists("/".join(outfile[:-1])):
			os.makedirs("/".join(outfile[:-1]))
		imagefile.save("/".join(outfile))
		progress.value += 1
		print(f"[{progress.value}/{total}] Processing images", end="\r")

def main():
	progress = Value("i", 0)
	imagepaths = list(Path("../Snow Station Photos 2023-2024").rglob("*.JPG"))

	global total
	total = len(imagepaths)

	# Split list across cores
	coretasks = []
	for i in range(os.cpu_count()):
		coretasks += [[]]
	for i, file in enumerate(imagepaths):
		coretasks[i % len(coretasks)] += [file]

	# Run processes
	processes = []
	for i, tasks in enumerate(coretasks):
		processes += [Process(target=filter_list, args=(tasks, progress))]
	for process in processes:
		process.start()
	for process in processes:
		process.join()

if __name__ == "__main__":
	main()