import json
import math
import os

# import cv2
# import numpy as np


def parseJson(filename="coco_output_manual.json"):
    f = open(filename)
    data = json.load(f)

    categories = {}
    for c in data["categories"]:
        categories[c["id"]] = c["name"]

    images = {}
    annotations = {}
    for i in data["images"]:
        images[i["id"]] = i["file_name"]
        annotations[i["id"]] = []

    for a in data["annotations"]:
        img_id = a["image_id"]
        cat_id = a["category_id"]
        bbox = a["bbox"]
        rot = a["attributes"]["rotation"]
        annotations[img_id].append((cat_id, rot, bbox))
    return categories, images, annotations


def getPoints(bbox):
    x_tl = bbox[0]
    y_tl = bbox[1]
    width = bbox[2]
    height = bbox[3]

    x_br = x_tl + width
    y_br = y_tl + height

    tl = (x_tl, y_tl)
    br = (x_br, y_br)
    tr = (x_br, y_tl)
    bl = (x_tl, y_br)
    return [tl, tr, br, bl]


def getMid(bbox):
    x_tl = bbox[0]
    y_tl = bbox[1]
    width = bbox[2]
    height = bbox[3]

    x_mid = x_tl + width / 2
    y_mid = y_tl + height / 2

    return (x_mid, y_mid)


def rotate_point(point, angle, midx, midy):

    old_x = point[0]
    old_y = point[1]

    old_cx = old_x - midx
    old_cy = old_y - midy

    angle_radians = math.radians(angle)

    angle_sin = math.sin(angle_radians)
    angle_cos = math.cos(angle_radians)

    new_cx = old_cx * angle_cos - old_cy * angle_sin
    new_cy = old_cx * angle_sin + old_cy * angle_cos

    new_x = new_cx + midx
    new_y = new_cy + midy

    point = (new_x, new_y)

    return point


def rotate_polygon(polygon, angle, midx, midy):

    new_points = []

    for p in polygon:
        new_p = rotate_point(p, angle, midx, midy)
        new_points.append(new_p)

    return new_points


# FOR DRAWING WITH CV2

# def pointsToInt(polygon):
#     new_points = []

#     for p in polygon:
#         new_p = [int(p[0]), int(p[1])]
#         new_points.append(new_p)
#     return new_points


# def drawAnnotation(img_id):
#     categories, images, annotations = parseJson()

#     bbox = annotations[img_id][0][2]
#     points = getPoints(bbox)
#     rot = annotations[img_id][0][1]
#     mid = getMid(bbox)
#     points = rotate_polygon(points, rot, mid[0], mid[1])
#     points = pointsToInt(points)

#     path = "./images/" + images[1]
#     image = cv2.imread(path)
#     window_name = "Image"

#     pts = np.array(points, np.int32)
#     pts.reshape(-1, 1, 2)

#     color = (255, 0, 0)
#     thickness = 2

#     image = cv2.polylines(image, [pts], True, color, thickness)

#     cv2.imshow(window_name, image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# drawAnnotation(1)


def yoloString(points, cat, diff):
    ret = ""
    for p in points:
        ret += str(p[0]) + ", " + str(p[1]) + ", "
    ret += cat + ", " + str(diff) + "\n"
    return ret


def outputYolo():
    categories, images, annotations = parseJson()

    path = "./annotations"
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    for img_id in images:
        filename = "./annotations/" + images[img_id][:-3] + "txt"
        lines = []
        for a in annotations[img_id]:
            cat_id = a[0]
            rot = a[1]
            bbox = a[2]
            points = getPoints(bbox)
            mid = getMid(bbox)
            points = rotate_polygon(points, rot, mid[0], mid[1])
            lines.append(yoloString(points, categories[cat_id], 1))
            # print(yoloString(points, cat, 0))
        with open(filename, "w") as f:
            f.writelines(lines)


outputYolo()
