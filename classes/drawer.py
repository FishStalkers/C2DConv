import cv2
import os
import numpy as np


class Drawer:
    """
    Utility class that draws the rotated annotations on the image for debugging.
    """

    def __init__(self, outpath):
        """
        Initializes and creates output directory to <outpath>/debug. Assumes images have
        already been copied to <outpath>/images.

        outpath: output directory of conversion session
        returns: None
        """
        self.outpath = outpath + "/debug"
        self.images_path = outpath + "/images"
        try:
            os.mkdir(self.outpath)
        except OSError as error:
            print(error)

    def pointsToInt(self, polygon):
        """
        Converts floating point coordinates to integer coordinates. Needed for
        CV2 drawing. Difference is likely undetecable by humans.

        polygon: list of floating point coordinates to convert
        returns: list of converted integer coordinates
        """
        new_points = []

        for p in polygon:
            new_p = [int(p[0]), int(p[1])]
            new_points.append(new_p)
        return new_points

    def drawAnnotation(self, boxes, image):
        """
        Uses OpenCV to draw bounding boxes on image contained in <outpath>/images. Writes
        drawn on images to <outpath>/debug.

        boxes: list of bounding boxes in the form of a list of points
        image: name of image file to draw on
        returns: None
        """
        img_path = os.path.join(self.images_path, image)
        if os.path.exists(img_path) and boxes:
            cv2image = cv2.imread(img_path)
            color = (0, 0, 255)
            thickness = 2

            for points in boxes:
                points = self.pointsToInt(points)
                points = np.array(points, np.int32)
                points.reshape(-1, 1, 2)
                cv2image = cv2.polylines(cv2image, [points], True, color, thickness)

            cv2.imwrite(os.path.join(self.outpath, image), cv2image)
