from .polygon import Polygon
from .regular_polygon import RegularPolygon
import numpy as np

class EquilateralTriangle(RegularPolygon):
    def __init__(self, side_length, **kwargs):
        super().__init__(3, side_length, **kwargs)

class IsoscelesTriangle(Polygon):
    def __init__(self, width, height, **kwargs):
        self.width = width
        self.height = height
        vertices = [[-width/2,0], [width/2,0], [0, height]]
        super().__init__(vertices, **kwargs)

