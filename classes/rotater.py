import math


class Rotater:
    def __init__(self):
        pass

    def getPoints(self, bbox):
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
        x_tl = bbox[0]
        y_tl = bbox[1]
        width = bbox[2]
        height = bbox[3]

        x_mid = x_tl + width / 2
        y_mid = y_tl + height / 2

        return (x_mid, y_mid)

    def rotatePoint(self, point, angle, midx, midy):

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

        new_points = []

        for p in polygon:
            new_p = self.rotatePoint(p, angle, midx, midy)
            new_points.append(new_p)

        return new_points
