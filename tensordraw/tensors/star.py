import numpy as np

from .polygon import Polygon
from ..utils import rotation

class Star(Polygon):
    def __init__(self, ntips, inner_radius, outer_radius, **kwargs):
        self.ntips = ntips
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        angle = np.pi/ntips
        inner_rescale = inner_radius/outer_radius
        vertices = []
        vtop = np.array([0, outer_radius])
        for i in range(self.ntips):
            vertices.append(rotation(2*i*angle)@vtop.T)
            vertices.append(inner_rescale*rotation((2*i+1)*angle)@vtop.T)

        super().__init__(vertices, **kwargs)


