# This is Filter Dot Pie, not Filter Dot Pee Why. My code, my rules.

import colorsys
import os
import multiprocessing
from PIL import Image
from pathlib import Path


class ImageFilterer():
    def __init__(self, filename):
        self.filename = filename
        self.imagefile = Image.open(filename)
        self.image = self.imagefile.load()
        self.savename = ".".join(self.filename.split(".")[:-1]) + "-filtered." + self.filename.split(".")[-1]


    def apply_filter(self):
        cores = os.cpu_count()

        processes = []

        for i in range(cores):
            processes += [multiprocessing.Process(target=self.apply_filter_thread, args=(i, cores))]

        for j in range(cores):
            processes[j].start()
        for j in range(cores):
            processes[j].join()
        
        self.imagefile.save(self.savename)


    def apply_filter_thread(self, core, cores):
        for y in range(core, self.imagefile.height, cores):
            for x in range(self.imagefile.width):
                pixel = list(colorsys.rgb_to_hsv(*self.image[x, y]))
                if (pixel[0] < 0.833):
                    self.image[x, y] = (0, 0, 0)
                    continue
                pixel[1] = 1
                pixel[2] = 255
                rgb = colorsys.hsv_to_rgb(*pixel)
                self.image[x, y] = (round(rgb[0]), round(rgb[1]), round(rgb[2]))

    def dump_rgb_values(self):
        for y in range(self.imagefile.height):
            for x in range(self.imagefile.width):
                print(f"X:{x}, Y:{y}, V:{self.image[x, y]}")