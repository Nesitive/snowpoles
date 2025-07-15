import os
import sys
import unittest
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

import filter

class FilterTest(unittest.TestCase):
	def test_filter(self):
		filterer = filter.ImageFilterer("tests/data/E9E/E9E_WSCT0209.JPG")
		filterer.apply_filter()
		filterer.dump_rgb_values()
		self.assertTrue(os.path.exists(filterer.savename))
		img = Image.open(filterer.savename)
		img.show()

	# def tearDown(self):
	# 	os.remove("tests/data/E9E/E9E_WSCT0209-filtered.JPG")