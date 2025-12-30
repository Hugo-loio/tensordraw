from abc import abstractmethod
import math

import numpy as np

from ..stroke_style import StrokeStyle
from ..fill_style import FillStyle
from .._placeable import Placeable

class BaseTensor(Placeable):
    def __init__(self, **kwargs):
        self.legs = []
        self.centroid = ([0,0])

        super().__init__(**kwargs)

    def leg_limtis(self, xmin, xmax, ymin, ymax, R):
        for leg in self.legs:
            left = R @ leg.tipleft().T
            right = R @ leg.tipright().T
            xmin = np.min([left[0], right[0], xmin])
            xmax = np.max([left[0], right[0], xmax])
            ymin = np.min([left[1], right[1], ymin])
            ymax = np.max([left[1], right[1], ymax])
        return [xmin, xmax, ymin, ymax]

    def path_leg_intersection(self, context, tleft, tright):
        ts = np.linspace(tright, tleft, 100)
        context.move_to(*self.path(ts[0]))
        for t in ts[1:]:
            context.line_to(*self.path(t))

    @abstractmethod
    # Parametric path (t in [0,1]) for the boundary of the tensor
    def path(self, t):
        pass

    # Limits of a rectangle surrounding the shape, with an applied rotation R
    @abstractmethod
    def limits(self, R):
        pass

    @abstractmethod
    def add_leg(self):
        pass

