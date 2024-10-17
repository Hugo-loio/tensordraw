from .polygon import Polygon
import numpy as np

class Rectangle(Polygon):
    def __init__(self, width, height, **kwargs):
        self.width = width
        self.height = height
        vertices = np.array([[width/2, height/2], 
                             [-width/2, height/2], 
                             [-width/2, -height/2],
                             [width/2, -height/2]])

        super().__init__(vertices, **kwargs)


    def set(self, **kwargs):
        super().set(**kwargs)
