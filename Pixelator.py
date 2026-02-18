from PIL import Image

from models.Color import Color


class Pixelator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.img = Image.new("RGB", (self.width, self.height), "white")

    def get_img(self):
        return self.img

    def put_pixel(self, x, y, color: Color):
        x = self.width // 2 + x
        x = int(x)
        y = self.height // 2 - y - 1
        y = int(y)
        self.img.putpixel((x, y), color.get_color())