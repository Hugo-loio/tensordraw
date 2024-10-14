from abc import ABC, abstractmethod
import math

import numpy as np

class BaseTensor(ABC):
    def __init__(self, **kwargs):
        self.fill_color = (0,0,1,1)
        self.stroke_color = (0,0,0,1)
        self.stroke_width = 1

        self.legs = []

        self.set(**kwargs)

    def set(self, **kwargs):
        if 'fill_color' in kwargs:
            self.fill_color = kwargs['fill_color']
        if 'stroke_color' in kwargs:
            self.stroke_color = kwargs['stroke_color']
        if 'stroke_width' in kwargs:
            self.stroke_width = kwargs['stroke_width']

    def leg_limtis(self, xmin, xmax, ymin, ymax, R):
        for leg in self.legs:
            left = R @ leg.tipleft().T
            right = R @ leg.tipright().T
            xmin = np.min([left[0], right[0], xmin])
            xmax = np.max([left[0], right[0], xmax])
            ymin = np.min([left[1], right[1], ymin])
            ymax = np.max([left[1], right[1], ymax])
        return [xmin, xmax, ymin, ymax]

    @abstractmethod
    def perimeter(self):
        # Include default perimeter by integrating the path
        pass

    @abstractmethod
    # Parametric path (t in [0,1]) for the boundary of the tensor
    def path(self, t):
        pass

    # Limits of a rectangle surrounding the shape, with an applied rotation R
    @abstractmethod
    def limits(self, R):
        pass

    @abstractmethod
    def draw(self, context):
        pass

    @abstractmethod
    def add_leg(self):
        pass

    #@abstractmethod
    #def draw_legs(self):
    #    pass
