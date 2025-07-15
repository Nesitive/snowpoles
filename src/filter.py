import colorsys
import os
import multiprocessing
from PIL import Image
from pathlib import Path

global imagefile
global image

def apply_filter(filename):
    global imagefile
    global image

    cores = os.cpu_count()

    imagefile = Image.open(filename)
    image = imagefile.load()

    processes = []

    for i in range(cores):
        processes += [multiprocessing.Process(target=apply_filter_thread, args=(i, cores))]

    for j in range(cores):
        processes[j].start()
    for j in range(cores):
        processes[j].join()

    savename = ".".join(filename.split(".")[:-1]) + "-filtered." + filename.split(".")[-1]
    imagefile.save(savename)

    return savename


def apply_filter_thread(core, cores):
    global imagefile
    global image

    for y in range(core, imagefile.height, cores):
        for x in range(imagefile.width):
            pixel = list(colorsys.rgb_to_hsv(*image[x, y]))
            if (pixel[0] < 0.833):
                image[x, y] = (0, 0, 0)
                continue
            pixel[1] = 1
            pixel[2] = 255
            rgb = colorsys.hsv_to_rgb(*pixel)
            image[x, y] = (round(rgb[0]), round(rgb[1]), round(rgb[2]))


def main():
    paths = list(Path(IMAGES_DIR).rglob("*.JPG"))
    files = []
    for path in paths:
        files += [str(path)[len(IMAGES_DIR) + 1 :]]
    for file in files:
        Path(FILTERED_DIR + "/" + file).parents[0].mkdir(parents=True, exist_ok=True)
    # Multiprocessing
    processes = []
    cores = os.cpu_count()
    for core, filename in enumerate(files):
        processes += [
            multiprocessing.Process(
                target=apply_filter, args=(filename, )
            )
        ]

    si = 0
    for i, process in enumerate(processes):
        if i != 0 and (i % cores == 0 or i == len(processes) - 1):
            if i == len(processes) - 1:
                ei = i + 1
            else:
                ei = i
            for j in range(si, ei):
                print("Processing", processes[j]._args[0])
                processes[j].start()
            for j in range(si, ei):
                processes[j].join()
            si = i

if (__name__ == "__main__"):
    main()
