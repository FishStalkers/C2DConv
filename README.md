# c2dconv: COCO to DOTA Annotation Format Converter

## Descrtiption

Converts manual annotations created in CVAT that are exported in COCO format to Yolov5-OBB annotation format with bbox rotations.

## Instructions

| NOTE: This section is still WIP! |
| -------------------------------- |

#### Usage:

    c2dconv.py -i <indir>                     # Convert to single dataset
    c2dconv.py -i <indir> -o <outdir>         # Convert to single dataset
    c2dconv.py -i <indir> -s                  # Convert to split dataset
    c2dconv.py -i <indir> -o <outdir> -s      # Convert to split dataset

#### Example Usage:

    c2dconv.py -i ./Verified_with_Attributes -s

#### Options:

    -h, --help              Show this help message and exits
    -i, --indir  <indir>    Place json files and images in <indir>
    -o, --outdir <outdir>   Outputs dataset to <outdir>, default is ./output
    -s, --split             Splits dataset
