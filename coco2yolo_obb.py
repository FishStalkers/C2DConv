import json
import math
import os
import shutil
import random

# import cv2
# import numpy as np

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

def rotatePoint(point, angle, midx, midy):

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

def rotatePolygon(polygon, angle, midx, midy):

    new_points = []

    for p in polygon:
        new_p = rotatePoint(p, angle, midx, midy)
        new_points.append(new_p)

    return new_points

def crawlPaths(startpath):
    json_paths = []
    img_paths = []
    txt_paths = []
    for root, dirs, files in os.walk(startpath):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".json"):
                json_paths.append(path)
            elif file.endswith(".jpg"):
                img_paths.append(path)
            elif file.endswith(".txt"):
                txt_paths.append(path)
    return json_paths, img_paths, txt_paths

def parseJson(filepath):
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

def yoloString(points, cat, diff):
    ret = ""
    for p in points:
        ret += str(p[0]) + ", " + str(p[1]) + ", "
    ret += cat + ", " + str(diff) + "\n"
    return ret

def outputYolo(outpath, json_paths):
    outpath += "/annotations"
    try:
        os.mkdir(outpath)
    except OSError as error:
        print(error)
    
    for path in json_paths:
        categories, images, annotations = parseJson(path)
        for img_id in images:
            filename = outpath + "/" + images[img_id][:-3] + "txt"
            lines = []
            for a in annotations[img_id]:
                cat_id = a[0]
                rot = a[1]
                bbox = a[2]
                points = getPoints(bbox)
                mid = getMid(bbox)
                points = rotatePolygon(points, rot, mid[0], mid[1])
                lines.append(yoloString(points, categories[cat_id], 1))
            with open(filename, "w") as f:
                f.writelines(lines)

def outputImgs(outpath, img_paths):
    outpath += "/images"
    try:
        os.mkdir(outpath)
    except OSError as error:
        print(error)
        
    for path in img_paths:
        shutil.copy(path, outpath)

def makeOutpath(outpath):
    try:
        os.mkdir(outpath)
        return outpath
    except OSError as error:
        dirname = outpath
        counter = 1
        while os.path.exists(outpath):
            outpath = dirname + " (" + str(counter) + ")"
            counter += 1
        try:
            os.mkdir(outpath)
            return outpath
        except OSError as error:
            print(error)

def splitDataset(outpath, shuffle = True, train_ratio=70, valid_ratio=20, test_ratio=10):
    if (train_ratio + valid_ratio + test_ratio != 100):
        raise Exception("Ratio split must add up to 100")
        
    train_path = outpath + "/train"
    valid_path = outpath + "/valid"
    test_path = outpath + "/test"
    
    try:
        os.mkdir(train_path)
        os.mkdir(train_path + "/annotations")
        os.mkdir(train_path + "/images")
        
        os.mkdir(valid_path)
        os.mkdir(valid_path + "/annotations")
        os.mkdir(valid_path + "/images")
        
        os.mkdir(test_path)
        os.mkdir(test_path + "/annotations")
        os.mkdir(test_path + "/images")
    except OSError as error:
        print(error)
    
    json_paths, img_paths, txt_paths = crawlPaths(outpath)
    
    if (len(img_paths) != len(txt_paths)):
        raise Exception("Number of annotations does not match number of images")
    
    img_paths = sorted(img_paths, key=lambda x: os.path.split(x)[-1])
    txt_paths = sorted(txt_paths, key=lambda x: os.path.split(x)[-1])
    
    if (shuffle):
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
        txt_filename = os.path.split(txt_path)[-1]
        img_filename = os.path.split(img_path)[-1]
        move_path = train_path + "/annotations"
        shutil.move(txt_path, move_path)
        move_path = train_path + "/images"
        shutil.move(img_path, move_path)
        
    for i in range(valid_num):
        txt_path = txt_paths.pop()
        img_path = img_paths.pop()
        txt_filename = os.path.split(txt_path)[-1]
        img_filename = os.path.split(img_path)[-1]
        move_path = valid_path + "/annotations"
        shutil.move(txt_path, move_path)
        move_path = valid_path + "/images"
        shutil.move(img_path, move_path)
        
    for i in range(test_num):
        txt_path = txt_paths.pop()
        img_path = img_paths.pop()
        txt_filename = os.path.split(txt_path)[-1]
        img_filename = os.path.split(img_path)[-1]
        move_path = test_path + "/annotations"
        shutil.move(txt_path, move_path)
        move_path = test_path + "/images"
        shutil.move(img_path, move_path)

    try:
        os.rmdir(outpath + "/annotations")
        os.rmdir(outpath + "/images")
    except OSError as error:
        print(error)
    
def run():
    json_paths, img_paths, txt_paths = crawlPaths('./VIP Data Exports')
    outpath = makeOutpath("./dataset")
    outputImgs(outpath, img_paths)
    outputYolo(outpath, json_paths)
    splitDataset(outpath)
    
run()



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