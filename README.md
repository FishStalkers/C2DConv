# c2dconv: COCO to DOTA Annotation Format Converter

## Descrtiption

Converts manual annotations created in CVAT that are exported in COCO format to Yolov5-OBB annotation format with bbox rotations.

## Instructions

| NOTE: This section is still WIP! |
| -------------------------------- |

#### Usage:

    c2dconv.py -i <indir>                       Convert <indir> to single dataset in ./output
    c2dconv.py -i <indir> -o <outdir>           Convert <indir> to single dataset in <outdir>
    c2dconv.py -i <indir> -s                    Convert <indir> to split dataset in ./output
    c2dconv.py -i <indir> -o <outdir> -s        Convert <indir> to split dataset in <outdir>
    c2dconv.py -z -i <indir>                    Unzip <indir> then convert to single dataset in ./output
    c2dconv.py -z -i <indir> -o <outdir>        Unzip <indir> then convert to single dataset in <outdir>
    c2dconv.py -z -i <indir> -s                 Unzip <indir> then convert to split dataset in ./output
    c2dconv.py -z -i <indir> -o <outdir> -s     Unzip <indir> then convert to split dataset in <outdir>

#### Example Usage:

    c2dconv.py -z -i ./Verified_with_Attributes.zip -s

#### Options:

    -h, --help              Show this help message and exits
    -z, --zip               Unzips <indir> and all inner zips before converting
    -i, --indir  <indir>    Place json files and images in <indir>
    -o, --outdir <outdir>   Outputs dataset to <outdir>, default is ./output
    -s, --split             Splits dataset
