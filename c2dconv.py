import sys
import getopt
import os

from classes.converter import Converter
from classes.crawler import Crawler
from classes.splitter import Splitter


def main(argv):
    # json_paths, img_paths, txt_paths = crawlPaths("./VIP Data Exports")
    # outpath = makeOutpath("./dataset")
    # outputImgs(outpath, img_paths)
    # outputYolo(outpath, json_paths)
    # splitDataset(outpath)
    # outputImgNameFile(outpath, img_paths)
    indir = ""
    outdir = "./output"
    isSplit = False

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    opts, args = getopt.getopt(argv, "hi:o:s", ["help", "indir=", "outdir=", "split"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                """
Description:
    Converts manual annotations created in CVAT that are exported in COCO format to Yolov5-OBB annotation format with bbox rotations.
Usage:
    coco2yolo_obb.py -i <indir>                     Convert to single dataset
    coco2yolo_obb.py -i <indir> -o <outdir>         Convert to single dataset
    coco2yolo_obb.py -i <indir> -s                  Convert to split dataset
    coco2yolo_obb.py -i <indir> -o <outdir> -s      Convert to split dataset
Example Usage:
    coco2yolo_obb.py -i ./Verified_with_Attributes -s
Options:
    -h, --help              Show this help message and exits
    -i, --indir  <indir>    Place json files and images in <indir> 
    -o, --outdir <outdir>   Outputs dataset to <outdir>, default is ./output
    -s, --split             Splits dataset
            """
            )
            sys.exit()
        elif opt in ("-i", "--indir"):
            indir = arg
        elif opt in ("-o", "--outdir"):
            outdir = arg
        elif opt in ("-s", "--split"):
            isSplit = True

    if not indir:
        print("Please specify input directory")
        sys.exit()

    if not os.path.exists(indir):
        print("Input directory does not exist")
        sys.exit()

    if os.path.exists(outdir) and outdir != "./output":
        print("Output directory does not exist")
        sys.exit()

    crawler = Crawler(startpath=indir)
    converter = Converter(outpath=outdir)

    json_paths, img_paths, txt_paths = crawler.crawlPaths()
    converter.generateSingleDataset(json_paths, img_paths)

    if isSplit:
        splitter = Splitter(outpath=converter.outpath)
        splitter.generateSplitDataset()


if __name__ == "__main__":
    main(sys.argv[1:])
