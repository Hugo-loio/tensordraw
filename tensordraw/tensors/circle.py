import numpy as np

from ._base_tensor import BaseTensor
from .leg import Leg
from ..utils import Position

class Circle(BaseTensor):
    def __init__(self, radius, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        if 'stroke_width' not in kwargs:
            self.stroke_width = radius/5

    def set(self, **kwargs):
        super().set(**kwargs)
        if 'radius' in kwargs:
            self.radius = kwargs['radius']

    def perimeter(self):
        return 2*np.pi*self.radius

    def add_leg(self, angle, tilt = 0, **kwargs):
        if 'length' in kwargs:
            length = kwargs['length'] + self.radius
        else:
            length = (4/3)*self.radius 

        tip_position = Position(np.cos(angle)*length, np.sin(angle)*length, angle - tilt)
        self.legs.append(Leg(self, tip_position, **kwargs))

    def path(self, t):
        return np.array([self.radius*np.cos(2*np.pi*t), self.radius*np.sin(2*np.pi*t)]) 

    def limits(self, R):
        xmin = -self.radius
        xmax = self.radius
        ymin = -self.radius
        ymax = self.radius
        return self.leg_limtis(xmin, xmax, ymin, ymax, R)

    def draw_leg(self, leg, context):
        context.set_source_rgba(*leg.color)
        context.save()
        tleft, tright = leg.intersections()
        left, right = self.path(tleft), self.path(tright)
        angleleft = np.arccos(left[0]/self.radius)
        if(left[1] < 0):
            angleleft = -angleleft
        angleright = np.arccos(right[0]/self.radius)
        if(right[1] < 0):
            angleright = -angleright
        context.arc(0, 0, self.radius - 0.01*self.stroke_width, angleright, angleleft)
        context.line_to(*leg.tipleft())
        context.line_to(*leg.tipright())
        context.close_path()
        context.fill()
        context.restore()

    def draw(self, context):
        # Outer circle
        context.set_source_rgba(*self.stroke_color)
        context.arc(0, 0, self.radius, 0, 2*np.pi)
        # Hollow interior due to Cairo's winding rule
        context.arc_negative(0, 0, self.radius - self.stroke_width, 0, -2*np.pi)
        context.fill()
        # Inner circle
        context.set_source_rgba(*self.fill_color)
        context.arc(0, 0, self.radius - self.stroke_width, 0, 2*np.pi)
        context.fill()

        for leg in self.legs:
            self.draw_leg(leg, context)
