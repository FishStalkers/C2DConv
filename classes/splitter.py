import os
import math
import random
import shutil
from classes.crawler import Crawler


class Splitter:
    def __init__(self, outpath):
        self.outpath = outpath
        self.crawler = Crawler(outpath)

    def makeSplitDirs(self):
        self.train_outpath = self.outpath + "/train"
        self.valid_outpath = self.outpath + "/valid"
        self.test_outpath = self.outpath + "/test"

        try:
            os.mkdir(self.train_outpath)
            os.mkdir(self.train_outpath + "/labelTxt")
            os.mkdir(self.train_outpath + "/images")

            os.mkdir(self.valid_outpath)
            os.mkdir(self.valid_outpath + "/labelTxt")
            os.mkdir(self.valid_outpath + "/images")

            os.mkdir(self.test_outpath)
            os.mkdir(self.test_outpath + "/labelTxt")
            os.mkdir(self.test_outpath + "/images")
        except OSError as error:
            print(error)

    def splitDataset(self, shuffle=True, train_ratio=70, valid_ratio=20, test_ratio=10):
        if train_ratio + valid_ratio + test_ratio != 100:
            raise Exception("Ratio split must add up to 100")

        json_paths, img_paths, txt_paths = self.crawler.crawlPaths()
        if len(img_paths) != len(txt_paths):
            shutil.rmtree(self.train_outpath)
            shutil.rmtree(self.valid_outpath)
            shutil.rmtree(self.test_outpath)
            raise Exception("Number of annotations does not match number of images")

        img_paths = sorted(img_paths, key=lambda x: os.path.split(x)[-1])
        txt_paths = sorted(txt_paths, key=lambda x: os.path.split(x)[-1])

        if shuffle:
            temp = list(zip(img_paths, txt_paths))
            random.shuffle(temp)
            img_paths, txt_paths = zip(*temp)
            img_paths, txt_paths = list(img_paths), list(txt_paths)

        train_num = math.floor(train_ratio / 100 * len(txt_paths))
        valid_num = math.floor(valid_ratio / 100 * len(txt_paths))
        test_num = math.floor(test_ratio / 100 * len(txt_paths))

        for i in range(train_num):
            txt_path = txt_paths.pop()
            img_path = img_paths.pop()
            move_path = self.train_outpath + "/labelTxt"
            shutil.move(txt_path, move_path)
            move_path = self.train_outpath + "/images"
            shutil.move(img_path, move_path)

        for i in range(valid_num):
            txt_path = txt_paths.pop()
            img_path = img_paths.pop()
            move_path = self.valid_outpath + "/labelTxt"
            shutil.move(txt_path, move_path)
            move_path = self.valid_outpath + "/images"
            shutil.move(img_path, move_path)

        for i in range(test_num):
            txt_path = txt_paths.pop()
            img_path = img_paths.pop()
            move_path = self.test_outpath + "/labelTxt"
            shutil.move(txt_path, move_path)
            move_path = self.test_outpath + "/images"
            shutil.move(img_path, move_path)

        try:
            os.rmdir(self.outpath + "/labelTxt")
            os.rmdir(self.outpath + "/images")
        except OSError as error:
            print(error)

    def generateSplitDataset(self, shuffle=True, train_ratio=70, valid_ratio=20, test_ratio=10):
        self.makeSplitDirs()
        self.splitDataset(shuffle, train_ratio, valid_ratio, test_ratio)
