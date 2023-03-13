import os
import json
import shutil
from classes.rotater import Rotater
from classes.crawler import Crawler
from classes.drawer import Drawer


class Converter:
    """
    Main driver class for converting COCO format to DOTA format.Rotations are
    calculated and added to the converted annotations in a specified output directory.
    Image files are also copied to a single unified dataset.
    For split datasets see "classes/splitter.py".
    """

    def __init__(self, outpath, isDraw):
        """
        Initialize new converter object. Outputs files to "<outpath>/converted".

        outpath: path of directory to output converted dataset
        returns: None
        """
        self.outpath = outpath + "/converted"
        self.isDraw = isDraw

    def makeOutputDir(self):
        """
        Makes output directory if it does not exist already.Supports multiple
        output directories with the same name by appending a number to the end
        of the directory name.

        returns: None
        """
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
        """
        Makes inner directories, "/images" and "/labelTxt", in output directory
        following the format of a single unified dataset.

        returns: None
        """
        self.images_outpath = self.outpath + "/images"
        self.labelTxt_outpath = self.outpath + "/labelTxt"
        try:
            os.mkdir(self.images_outpath)
            os.mkdir(self.labelTxt_outpath)
        except OSError as error:
            print(error)

    def parseJson(self, filepath):
        """
        Parses a single json file in COCO Format and returns dictionaries of
        found categories, images, and annotations. The image dictionary holds
        the image file names per annotion. The annotation dictionary holds the
        corresponding image, category, rotation, and bounding box per annotation.
        The categories dictionary simply maps category ids to category names.

        filepath: path of json file to parse
        returns: tuple of dictionaries of categories, images, and annotations
        """
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

    def dotaString(self, points, cat, diff):
        """
        Generates a string in the format of a single line in a DOTA labelTxt file.

        points: list of points in the form of a list of tuples of the form (x, y)
        cat: category name
        diff: difficulty level (set to 1 for all converted annotations)
        returns: string in the format of a single line in a DOTA labelTxt file
        """
        ret = ""
        for p in points:
            ret += str(p[0]) + " " + str(p[1]) + " "
        ret += cat + " " + str(diff) + "\n"
        return ret

    def outputLabelTxt(self, json_paths):
        """
        Takes a list of json file paths and parses each one. The parsed data is then
        converted to DOTA format and output as a txt file to the labelTxt directory.
        Each txt file is named after the corresponding image file and contains all
        annotations for that image.

        json_paths: list of paths of json files to parse
        returns: None
        """
        rotater = Rotater()
        if self.isDraw:
            drawer = Drawer(self.outpath)
        for path in json_paths:
            categories, images, annotations = self.parseJson(filepath=path)
            for img_id in images:
                filename = self.labelTxt_outpath + "/" + images[img_id][:-3] + "txt"
                lines = []
                boxes = []
                for a in annotations[img_id]:
                    cat_id = a[0]
                    rot = a[1]
                    bbox = a[2]
                    points = rotater.getPoints(bbox)
                    mid = rotater.getMid(bbox)
                    points = rotater.rotatePolygon(points, rot, mid[0], mid[1])
                    boxes.append(points)
                    lines.append(self.dotaString(points, categories[cat_id], 1))

                with open(filename, "w") as f:
                    f.writelines(lines)
                if self.isDraw:
                    drawer.drawAnnotation(boxes, images[img_id])

    def outputImages(self, img_paths):
        """
        Copies all image files to the output images directory.

        img_paths: list of paths of image files to copy
        returns: None
        """
        for path in img_paths:
            shutil.copy(path, self.images_outpath)

    def outputImgNameFile(self, img_paths):
        """
        Creates a text file containing the names of all image files in the dataset.
        Needed for the DOTA evaluation script and Yolov5-OBB specific metrics. This
        file is output to the root of the output directory.

        img_paths: list of paths of image files to copy
        returns: None
        """
        lines = []
        for img in img_paths:
            filename = os.path.split(img)[-1][:-3]
            lines.append(filename + "\n")
        with open(os.path.join(self.outpath, "imgnamefile.txt"), "w") as f:
            f.writelines(lines)

    def check(self):
        """
        Checks if the number of txt files and image files match and prints a warning.
        Crawls the output directory for txt and image files then counts. Could use
        optimization, but this was the best way to make sure the number of txt files
        matched the number of image files.

        returns: None
        """
        crawler = Crawler(self.outpath)
        json_paths, img_paths, txt_paths = crawler.crawlPaths()

        if len(img_paths) != len(txt_paths):
            print(f"Warning: Number of txt files ({len(txt_paths)}) and image files ({len(img_paths)}) does not match")

    def generateSingleDataset(self, json_paths, img_paths, check=True):
        """
        Main driver function for converting a dataset to DOTA format. Creates necessary
        output directories, outputs labelTxt files, outputs image files, and checks if
        the number of txt files and image files match.

        If check is set to False, the number of txt files and image files will not be checked.
        Check can be set to false if dataset is being split as splitDataset() will perform the
        same check and the extra crawling is expensive and redundant.

        json_paths: list of paths of COCO json files to parse, convert, and output
        img_paths: list of paths of image files to copy
        check: boolean indicating whether to check if the number of txt files and image
        returns: None
        """
        self.makeOutputDir()
        self.makeSingleDir()
        self.outputImages(img_paths)
        self.outputLabelTxt(json_paths)

        if check:
            self.check()
