# This is Filter Dot Pie, not Filter Dot Pee Why. My code, my rules.

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