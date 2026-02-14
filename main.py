from PIL import Image
from numpy._utils._pep440 import Infinity

from models.Color import Color
from utils import Vec, Sphere, canvas_to_viewport, trace_ray, Light, LIGHT_AMBIENT, LIGHT_POINT, LIGHT_DIRECTION, \
    multiply_mv


# noinspection PyShadowingNames
def put_pixel(x, y, width, height, color: Color):
    x = width // 2 + x
    x =int(x)
    y = height // 2 - y - 1
    y = int(y)
    img.putpixel((x, y), color.get_color())

if __name__ == '__main__':
    width, height = 500, 500
    img = Image.new("RGB", (width, height), "white")
    center_x = (width // 2)
    center_y = (height // 2)
    # color = Color(100, 120, 200)
    # img.putpixel((center_x, center_y), color.get_color())
    # img.show()
    viewport_size = 1
    viewport_projection_plane_z = 1
    camera_position = Vec(0, -0, 0)
    background_color = Color(255, 255, 255)
    rot_mat = [
              [1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]
    ]
    for x in range(-center_x, center_x):
        for y in range(-center_y, center_y):
            direction = canvas_to_viewport(x, y, projection_plane_z=viewport_projection_plane_z, viewport_size=viewport_size, canvas_width=width, canvas_height=height)
            direction = multiply_mv(rot_mat, direction)
            color = trace_ray(camera_position, direction, 1, Infinity, 1)
            put_pixel(x, y, width, height, color)

    img.show()





