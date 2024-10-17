import numpy as np

from .polygon import Polygon
from ..utils import rotation

class RegularPolygon(Polygon):
    def __init__(self, nsides, side_length, **kwargs):
        self.nsides = nsides
        self.side_length = side_length
        # cos angle/2 = length/2radius
        self.angle = 2*np.pi/nsides
        self.radius = side_length/(2*np.cos(self.angle/2))
        vertices = []
        vertices = [rotation(i*self.angle) @ np.array([0,self.radius]) for i in range(nsides)]

        super().__init__(vertices, **kwargs)


