import os
import json
import shutil
from classes.rotater import Rotater


class Converter:
    def __init__(self, outpath="./output"):
        self.outpath = outpath + "/converted"
        self.rotater = Rotater()

    def makeOutputDir(self):
        try:
            os.mkdir(self.outpath)
        except OSError as error:
            dirname = self.outpath
            counter = 1
            while os.path.exists(self.outpath):
                self.outpath = dirname + " (" + str(counter) + ")"
                counter += 1
            try:
                os.mkdir(self.outpath)
            except OSError as error:
                print(error)

    def makeSingleDir(self):
        self.images_outpath = self.outpath + "/images"
        self.labelTxt_outpath = self.outpath + "/labelTxt"
        try:
            os.mkdir(self.images_outpath)
            os.mkdir(self.labelTxt_outpath)
        except OSError as error:
            print(error)

    def parseJson(self, filepath):
        f = open(filepath)
        data = json.load(f)

        categories = {}
        for c in data["categories"]:
            categories[c["id"]] = c["name"]

        images = {}
        annotations = {}
        for i in data["images"]:
            images[i["id"]] = os.path.split(i["file_name"])[-1]
            annotations[i["id"]] = []

        for a in data["annotations"]:
            img_id = a["image_id"]
            cat_id = a["category_id"]
            bbox = a["bbox"]
            rot = a["attributes"]["rotation"]
            annotations[img_id].append((cat_id, rot, bbox))
        return categories, images, annotations

    def yoloString(self, points, cat, diff):
        ret = ""
        for p in points:
            ret += str(p[0]) + " " + str(p[1]) + " "
        ret += cat + " " + str(diff) + "\n"
        return ret

    def outputLabelTxt(self, json_paths):
        for path in json_paths:
            categories, images, annotations = self.parseJson(filepath=path)
            for img_id in images:
                filename = self.labelTxt_outpath + "/" + images[img_id][:-3] + "txt"
                lines = []
                for a in annotations[img_id]:
                    cat_id = a[0]
                    rot = a[1]
                    bbox = a[2]
                    points = self.rotater.getPoints(bbox)
                    mid = self.rotater.getMid(bbox)
                    points = self.rotater.rotatePolygon(points, rot, mid[0], mid[1])
                    lines.append(self.yoloString(points, categories[cat_id], 1))
                with open(filename, "w") as f:
                    f.writelines(lines)

    def outputImages(self, img_paths):
        for path in img_paths:
            shutil.copy(path, self.images_outpath)

    def outputImgNameFile(self, img_paths):
        lines = []
        for img in img_paths:
            filename = os.path.split(img)[-1][:-3]
            lines.append(filename + "\n")
        with open(os.path.join(self.outpath, "imgnamefile.txt"), "w") as f:
            f.writelines(lines)

    def generateSingleDataset(self, json_paths, img_paths):
        self.makeOutputDir()
        self.makeSingleDir()
        self.outputLabelTxt(json_paths)
        self.outputImages(img_paths)
        self.outputImgNameFile(img_paths)
