from models.point import Point
from utils import viewport_to_canvas


class Vertex:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


    def project_vertex(self, width, height, projection_plane_z):
        return viewport_to_canvas(Point(self.x*projection_plane_z/self.z, self.y*projection_plane_z/self.z), width,
                                  height, projection_plane_z)

    def add(self, v):
        return Vertex(self.x+v.x, self.y+v.y, self.z+v.z)

    def mul(self, n):
        return Vertex(self.x*n, self.y*n, self.z*n)

class Vertex4(Vertex):
    def __init__(self, x: float, y: float, z: float, w: float):
        super().__init__(x, y, z)
        self.w = w
