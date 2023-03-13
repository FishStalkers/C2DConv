import math


class Rotater:
    """
    Rotater provides utility functions to rotate bounding boxes around
    their midpoint by a given angle.
    """

    def getPoints(self, bbox):
        """
        Takes in a bounding box in COCO format and returns the 4 points
        of the bbox in the form of a list of tuples.

        bbox: bounding box in COCO format
        returns: list of tuples of the form [(x_tl, y_tl), (x_tr, y_tr), (x_br, y_br), (x_bl, y_bl)]
        """
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

    def getMid(self, bbox):
        """
        Gets the midpoint of a bounding box in COCO format.

        bbox: bounding box in COCO format
        returns: midpoint of bounding box in tuple of the form (x_mid, y_mid)
        """
        x_tl = bbox[0]
        y_tl = bbox[1]
        width = bbox[2]
        height = bbox[3]

        x_mid = x_tl + width / 2
        y_mid = y_tl + height / 2

        return (x_mid, y_mid)

    def rotatePoint(self, point, angle, midx, midy):
        """
        Rotates a point around a midpoint by a given angle.

        point: point to be rotated
        angle: angle to rotate point by
        midx: x coordinate of midpoint
        midy: y coordinate of midpoint
        returns: rotated point in tuple of the form (x, y)
        """
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

    def rotatePolygon(self, polygon, angle, midx, midy):
        """
        Rotates a polygon defined by it's points around it's midpoint
        by a given angle. We use this to rotate the bounding box of an
        object. This function is able to rotate any polygon, however, we
        only use it for rectangular bounding boxes.

        polygon: list of points defining the polygon
        angle: angle to rotate polygon by
        midx: x coordinate of midpoint
        midy: y coordinate of midpoint
        """
        new_points = []

        for p in polygon:
            new_p = self.rotatePoint(p, angle, midx, midy)
            new_points.append(new_p)

        return new_points
