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