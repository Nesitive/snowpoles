import filecmp
import os
from shutil import copyfile, rmtree
import sys
import unittest
from cv2 import imread

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")


import train


class TrainingTest(unittest.TestCase):
    def setUp(self):
        copyfile("tests/data/test-labels.csv", "tests/data/labels.csv")
        copyfile("tests/data/test-pole_metadata.csv", "tests/data/pole_metadata.csv")
        os.mkdir("tests/models/trained")

    def test_train(self):
        train.train("tests/models/trained", "cpu", "models/CO_and_WA_model.pth", 0.0001, 20, "tests/data", True, 4, False)
        self.assertTrue(os.path.exists("tests/models/model.pth"))
        self.assertTrue(os.path.exists("tests/models/loss.csv"))

    def test_train_filter(self):
        train.train("tests/models/trained", "cpu", "models/CO_and_WA_model.pth", 0.0001, 20, "tests/data", True, 4, True)
        print(cv2.imread("tests/models/val_epoch_0.png")[122, 122])
        self.assertTrue(os.path.exists("tests/models/model.pth"))
        self.assertTrue(os.path.exists("tests/models/loss.csv"))

    def tearDown(self):
        os.remove("tests/data/labels.csv")
        os.remove("tests/data/pole_metadata.csv")
        rmtree("tests/models/trained")
