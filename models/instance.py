from models.matrix import Matrix
from models.model import Model

identity_matrix = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


class Instance:
    def __init__(self, model: Model, position, orientation=None, scale=None):
        self.model = model
        self.position = position
        self.orientation = orientation if orientation is not None else identity_matrix
        self.scale = scale if scale is not None else 1.0
        self.transform = Matrix.multiply_mm4(Matrix.make_translation_matrix(self.position),
                                             Matrix.multiply_mm4(self.orientation, Matrix.make_scale_matrix(self.scale)))