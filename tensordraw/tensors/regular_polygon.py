import numpy as np

from .polygon import Polygon
from ..utils import rotation

class RegularPolygon(Polygon):
    def __init__(self, nsides, side_length, **kwargs):
        self.nsides = nsides
        self.side_length = side_length
        rotation_angle = 2*np.pi/nsides
        interior_angle = np.pi*(nsides-2)/nsides
        # cos angle/2 = length/2radius
        self.radius = side_length/(2*np.cos(interior_angle/2))
        vertices = [rotation(i*rotation_angle) @ np.array([0,self.radius]) for i in range(nsides)]

        super().__init__(vertices, **kwargs)


