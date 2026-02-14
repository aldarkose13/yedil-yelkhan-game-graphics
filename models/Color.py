class Color:
    def __init__(self, r: int, g: int, b: int):
        # Convert to int and clamp between 0-255
        self.r = int(max(0, min(255, r)))
        self.g = int(max(0, min(255, g)))
        self.b = int(max(0, min(255, b)))

    def get_color(self) -> tuple:
        return self.r, self.g, self.b

    def mul(self, n: float) -> 'Color':
        # Ensure the new values are passed back as integers
        return Color(int(self.r * n), int(self.g * n), int(self.b * n))

    def add(self, color : 'Color') -> 'Color':
        return Color(self.r + color.r, self.g + color.g, self.b + color.b)