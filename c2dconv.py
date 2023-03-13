import sys
import getopt
import os

from classes.converter import Converter
from classes.crawler import Crawler
from classes.splitter import Splitter
from classes.unzipper import Unzipper


def main(argv):
    # Initializing default values for arguements
    indir = ""
    outdir = "./output"
    isSplit = False
    isZip = False
    isDraw = False

    # Make default output directory if it does not exist already
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # Scan for arguments and set appropriate variables
    opts, args = getopt.getopt(argv, "hi:zo:sd", ["help", "indir=", "zip", "outdir=", "split", "draw"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                """
Description:
    Converts manual annotations created in CVAT that are exported in COCO format to Yolov5-OBB annotation format with bbox rotations.
Usage:
    c2dconv.py -i <indir>                       Convert <indir> to single dataset in ./output
    c2dconv.py -i <indir> -o <outdir>           Convert <indir> to single dataset in <outdir>
    c2dconv.py -i <indir> -s                    Convert <indir> to split dataset in ./output
    c2dconv.py -i <indir> -o <outdir> -s        Convert <indir> to split dataset in <outdir>
    c2dconv.py -z -i <indir>                    Unzip <indir> then convert to single dataset in ./output
    c2dconv.py -z -i <indir> -o <outdir>        Unzip <indir> then convert to single dataset in <outdir>
    c2dconv.py -z -i <indir> -s                 Unzip <indir> then convert to split dataset in ./output
    c2dconv.py -z -i <indir> -o <outdir> -s     Unzip <indir> then convert to split dataset in <outdir>
Example Usage:
    c2dconv.py -z -i ./Verified_with_Attributes.zip -s
Options:
    -h, --help              Show this help message and exits
    -z, --zip               Unzips <indir> and all inner zips before converting
    -i, --indir  <indir>    Place json files and images in <indir>, cannot contain "debug" in name
    -o, --outdir <outdir>   Outputs dataset to <outdir>, default is ./output, cannot contain "debug" in name
    -s, --split             Splits dataset
    -d, --draw              Draws rotated bounding boxes on images for debugging
            """
            )
            sys.exit()
        elif opt in ("-z", "--zip"):
            isZip = True
        elif opt in ("-i", "--indir"):
            indir = arg
        elif opt in ("-o", "--outdir"):
            outdir = arg
        elif opt in ("-s", "--split"):
            isSplit = True
        elif opt in ("-d", "--draw"):
            isDraw = True

    # Basic error checking
    if not indir:
        print("Please specify input directory")
        sys.exit()

    if not os.path.exists(indir):
        print("Input directory does not exist")
        sys.exit()

    if os.path.exists(outdir) and outdir != "./output":
        print("Output directory does not exist")
        sys.exit()

    if isZip and not indir.endswith(".zip"):
        print("Input directory must be a zip file when setting -z or --zip")
        sys.exit()

    if not isZip and indir.endswith(".zip"):
        print("Input directory must be a directory when not setting -z or --zip")
        sys.exit()

    # Unzips indir if isZip is True and resets indir to the unzippes directory
    if isZip:
        unzipper = Unzipper(file=indir)
        unzipper.unzip()
        indir = unzipper.targetdir

    # Create a crawler and search for json, image, and text files in indir
    crawler = Crawler(startpath=indir)
    json_paths, img_paths, txt_paths = crawler.crawlPaths()

    # Create a converter and generate a single dataset from json_paths
    # and img_paths found by the crawler
    converter = Converter(outpath=outdir, isDraw=isDraw)
    converter.generateSingleDataset(json_paths, img_paths)

    # Split dataset if -s or --split flag is set
    try:
        if isSplit:
            splitter = Splitter(outpath=converter.outpath)
            splitter.generateSplitDataset()
    except Exception as e:
        print(e.args[0])
    finally:
        # Creates a text file containing the names of all images in the dataset
        # Needed for receiving Yolov5-OBB specific metrics
        converter.outputImgNameFile(img_paths)

        # Cleans up the unzipped directory if isZip is True
        if isZip:
            unzipper.cleanup()

    print(f'Success: Finished converting "{indir}" to "{converter.outpath}"')


if __name__ == "__main__":
    main(sys.argv[1:])
