import math
from typing import Any

from Pixelator import Pixelator
from models.Color import Color
from models.Point import Point


class Rasterizer:
    def __init__(self, pixelator : Pixelator):
        self.pixelator = pixelator

    @staticmethod
    def interpolate(i0 : int, d0 : int, i1 : int, d1 : int) -> list[int] | None:
        if i0==i1:
            return [d0]
        values = []
        a = (d1-d0) / (i1-i0)
        d = d0
        for i in range(i0, i1+1):
            values.append(d)
            d += a
        return values

    def draw_line(self, p0 : Point, p1 : Point, color: Color):
        dx = p1.x - p0.x
        dy = p1.y - p0.y
        if math.fabs(dx)>math.fabs(dy):
            if dx<0:
                swap = p0
                p0 = p1
                p1 = swap
            ys = Rasterizer.interpolate(p0.x, p0.y, p1.x, p1.y)
            for x in range(p0.x, p1.x+1):
                self.pixelator.put_pixel(x, int(ys[(x - p0.x)]), color)
        else:
            if dy<0:
                swap = p0
                p0 = p1
                p1 = swap
            xs = Rasterizer.interpolate(p0.y, p0.x, p1.y, p1.x)
            for y in range(p0.y, p1.y+1):
                self.pixelator.put_pixel(int(xs[(y-p0.y)]), y, color)


    def draw_wire_frame_triangle(self, p0 : Point, p1 : Point, p2 : Point, color: Color):
        self.draw_line(p0, p1, color)
        self.draw_line(p1, p2, color)
        self.draw_line(p0, p2, color)

    @staticmethod
    def sort_points(p0, p1, p2):
        if p1.y < p0.y :swap = p0; p0 = p1; p1 = swap
        if p2.y < p0.y :swap = p0; p0 = p2; p2 = swap
        if p2.y < p1.y :swap = p1; p1 = p2; p2 = swap
        return p0, p1, p2


    def draw_filled_triangle(self, p0 : Point, p1 : Point, p2 : Point, color: Color):
        p0, p1, p2 = Rasterizer.sort_points(p0, p1, p2)
        x01 = Rasterizer.interpolate(p0.y, p0.x, p1.y, p1.x)
        x12 = Rasterizer.interpolate(p1.y, p1.x, p2.y, p2.x)
        x02 = Rasterizer.interpolate(p0.y, p0.x, p2.y, p2.x)
        x01.pop()
        x012 = x01 + x12
        m = len(x02)//2 | 0
        if x02[m] < x012[m]:
            x_left = x02
            x_right = x012
        else:
            x_left = x012
            x_right = x02
        for y in range(p0.y, p2.y+1):
            xl = x_left[y - p0.y]
            xr = x_right[y - p0.y]
            x_start = int(min(xl, xr))
            x_end = int(max(xl, xr))
            for x in range(x_start, x_end):
                self.pixelator.put_pixel(x, y, color)