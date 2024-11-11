import numpy as np

from ._base_tensor import BaseTensor
from .leg import Leg
from ..utils import Position
from ..utils import rotation

class Circle(BaseTensor):
    def __init__(self, radius, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        if self.stroke_style.default['width']:
            self.stroke_style.set(width = radius/5)

    def perimeter(self):
        return 2*np.pi*self.radius

    def add_leg(self, angle, tilt = 0, **kwargs):
        if 'length' in kwargs:
            length = kwargs['length'] 
        else:
            length = self.radius/3

        leg_dir = rotation(angle + tilt) @ np.array([1,0])
        base_point = self.path(angle/(2*np.pi))

        tip_position = Position(*(base_point + length*leg_dir), angle + tilt)
        self.legs.append(Leg(self, tip_position, base_point, **kwargs))

    def path(self, t):
        return np.array([self.radius*np.cos(2*np.pi*t), self.radius*np.sin(2*np.pi*t)]) 

    def limits(self, R):
        xmin = -self.radius - self.stroke_style.width/2
        xmax = self.radius + self.stroke_style.width/2
        ymin = -self.radius - self.stroke_style.width/2
        ymax = self.radius + self.stroke_style.width/2
        return self.leg_limtis(xmin, xmax, ymin, ymax, R)

    def path_leg_intersection(self, context, tleft, tright):
        context.arc(0, 0, self.radius, 2*np.pi*tright, 2*np.pi*tleft)

    def draw(self, context):
        context.arc(0, 0, self.radius, 0, 2*np.pi)

        self.stroke_and_fill(context)

        for leg in self.legs:
            leg.draw(context)
