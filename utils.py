import math
from msilib.schema import IniFile

from numpy._utils._pep440 import Infinity

from models.color import Color

LIGHT_AMBIENT = 0
LIGHT_POINT = 1
LIGHT_DIRECTION = 2
EPSILON = 0.001


class Vec:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_z(self) -> float:
        return self.z

# Vector functions
def dot(v1: Vec, v2: Vec) -> float:
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def add(v1: Vec, v2: Vec) -> Vec:
    return Vec(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def subtract(v1: Vec, v2: Vec) -> Vec:
    return Vec(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def multiply(v1: Vec, n: float) -> Vec:
    return Vec(v1.x * n, v1.y * n, v1.z * n)

def length(v: Vec) -> float:
    return math.sqrt(dot(v, v))

def reflect_ray(v1:Vec, v2: Vec) -> Vec:
    return subtract(multiply(v2, 2*dot(v1, v2)), v1)

class Sphere:
    def __init__(self, center: Vec, radius: float, color: object, specular: float | None = None,
                 reflective:float| None = None, transparency: float | None = None):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
        self.reflective = reflective
        self.transparency = transparency

    def get_center(self) -> Vec:
        return self.center

    def get_radius(self) -> float:
        return self.radius

    def get_color(self) -> object:
        return self.color

    def get_specular(self) -> float | None:
        return self.specular

    def get_reflective(self) -> float | None:
        return  self.reflective

    def get_transparency(self) -> float | None:
        return self.transparency

class Light:
    def __init__(self, ltype: int, intensity: float, position: Vec | None = None):
        self.ltype = ltype
        self.intensity = intensity
        self.position = position



spheres = [
        Sphere(center=Vec(0, -1, 3), radius=1, color=Color(255, 0, 0), specular = 10, reflective=0.12,
               transparency=0.8),
        Sphere(center=Vec(-2, 0, 4), radius=1, color=Color(0, 255, 0), specular=10, reflective=0.09,
               transparency=0),
        Sphere(center=Vec(2, 0, 4), radius=1, color=Color(0, 0, 255), specular=20, reflective=0.02,
               transparency=0),
        Sphere(center=Vec(0, -5001, 0), radius=5000, color=Color(255, 255, 0), specular=1, reflective=0.05,
               transparency=0),

    ]
lights = [
    Light(LIGHT_AMBIENT, 0.2),
    Light(LIGHT_POINT, 0.6, Vec(2,1,0)),
    Light(LIGHT_DIRECTION, 0.2, Vec(1,4,4)),
]



def canvas_to_viewport(x, y, projection_plane_z, viewport_size, canvas_width, canvas_height):
    return Vec(x*viewport_size/canvas_width, y*viewport_size/canvas_height, projection_plane_z)

def multiply_mv(rotation_matrix:list, vec : Vec) -> Vec:
    result = [0,0,0]
    vec = [vec.x, vec.y, vec.z]
    for i in range(0, 3):
        for j in range(0, 3):
            result[i] = result[i] + (vec[j] * rotation_matrix[i][j])
    return Vec(result[0], result[1], result[2])

def intersect_ray_sphere(origin, direction, sphere):
    oc = subtract(origin, sphere.center)

    a = dot(direction, direction)
    b = 2*dot(oc, direction)
    c = dot(oc, oc) - sphere.radius * sphere.radius

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return [Infinity, Infinity]

    t1 = (-b + math.sqrt(discriminant))/(2*a)
    t2 = (-b - math.sqrt(discriminant))/(2*a)

    return [t1, t2]



def compute_lighting(point, normal: Vec, view: Vec, specular, ligths):
    intensity = 0
    length_n = length(normal)
    length_v = length(view)
    for i in range(0, len(ligths)):
        light = ligths[i]
        if light.ltype == LIGHT_AMBIENT:
            intensity += light.intensity
            continue
        vec_l = None
        t_max = None
        if light.ltype == LIGHT_POINT:
            vec_l = subtract(light.position, point)
            t_max = 1.0
        else:
            # Directional light
            vec_l = light.position
            t_max = Infinity

        # shadow check
        blocker = closest_intersection(point, vec_l, EPSILON, t_max)
        if blocker:
            continue
        n_dot_l = dot(vec_l, normal)
        if n_dot_l > 0:
            intensity += light.intensity * n_dot_l / (length_n * length(vec_l))

        if specular != -1:
            vec_r = multiply(normal, 2.0*n_dot_l)
            vec_r = subtract(vec_r, vec_l)
            r_dot_v = dot(vec_r, view)
            if r_dot_v > 0:
                intensity += light.intensity * math.pow((r_dot_v/ length(vec_l) * length_v), specular)

    return intensity


def closest_intersection(origin, direction : Vec, min_t, max_t):
    closest_t = Infinity
    closest_sphere = None
    for t in range(0, len(spheres)):
        ts = intersect_ray_sphere(origin, direction, spheres[t])
        if ts[0] < closest_t and min_t < ts[0] and ts[0] < max_t:
            closest_t = ts[0]
            closest_sphere = spheres[t]
        if ts[1] < closest_t and min_t < ts[1] and ts[1] < max_t:
            closest_t = ts[1]
            closest_sphere = spheres[t]

    if closest_sphere:
        return [closest_sphere, closest_t]
    return None

def trace_ray(origin, direction : Vec, min_t, max_t, depth):
    intersection = closest_intersection(origin, direction, min_t, max_t)

    if intersection is None:
        return Color(255,255,255)

    closest_sphere = intersection[0]
    closest_t = intersection[1]
    point = add(origin, multiply(direction, closest_t))
    normal = subtract(point, closest_sphere.center)
    normal = multiply(normal, 1.0/length(normal))

    view = multiply(direction, -1)
    lighting = compute_lighting(point, normal, view, closest_sphere.specular, lights)
    local_color = closest_sphere.color.mul(lighting)
    if depth <=0:
        return local_color
    reflective = closest_sphere.get_reflective() or 0
    transparency = closest_sphere.get_transparency() or 0
    reflected_ray = reflect_ray(view, normal)
    reflected_color = trace_ray(point, reflected_ray, EPSILON, Infinity, depth-1)
    refracted_color = Color(0,0,0)
    if transparency > 0:
        refracted_color = trace_ray(point, direction, EPSILON, Infinity, depth-1)
    local_contribution = local_color.mul(1-reflective)
    reflected_contribution = reflected_color.mul(reflective)
    refracted_contribution = refracted_color.mul(transparency)
    return local_contribution.add(reflected_contribution).add(refracted_contribution)
