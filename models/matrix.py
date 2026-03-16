import math

from models.vertex import Vertex4
from utils import Vec


class Matrix:
    def __init__(self, rows:list):
        self.twod_arr =  rows

    @staticmethod
    def identity():
        return Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def make_oy_rotation_matrix(degrees):
        radians = math.radians(degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        return Matrix([[cos, 0, -sin, 0], [0, 1, 0, 0], [sin, 0, cos, 0], [0, 0, 0, 1] ])

    @staticmethod
    def make_translation_matrix(translation):
        return Matrix([[1, 0, 0, translation.x], [0, 1, 0, translation.y], [0, 0, 1, translation.z], [0, 0, 0,  1]])

    @staticmethod
    def make_scale_matrix(scale):
        return Matrix([[scale, 0, 0, 0], [0, scale, 0, 0], [0, 0, scale, 0], [0, 0, 0, 1]])

    @staticmethod
    def multiply_mv(mat4x4, vec4):
        result = [0,0,0,0]
        vec = [vec4.x, vec4.y, vec4.z, vec4.w]
        for i in range(0, 4):
            for j in range(0, 4):
                result[i] = result[i] + (vec[j] * mat4x4.twod_arr[i][j])
        return Vertex4(result[0], result[1], result[2], result[3])

    @staticmethod
    def multiply_mm4(mat_a,mat_b):
        result = Matrix([
            [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]
                         ])
        for i in range(0,4):
            for j in range(0,4):
                for k in range(0,4):
                    result.twod_arr[i][j] = result.twod_arr[i][j] + (mat_a.twod_arr[i][k] * mat_b.twod_arr[k][j])
        return result

    @staticmethod
    def transposed(mat):
        result = Matrix([
            [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]
        ])
        for i in range(0,4):
            for j in range(0,4):
                result.twod_arr[j][i] = mat.twod_arr[i][j]
        return result