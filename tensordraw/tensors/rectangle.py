from ._base_tensor import BaseTensor
from ..utils import rounded_rectangle
import numpy as np

class Rectangle(BaseTensor):
    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.min_length = np.min([width, height])

        if 'stroke_width' not in kwargs:
            self.stroke_width = self.min_length/10

        self.corner_radius = 2*self.stroke_width

        if 'corner_radius' in kwargs:
            self.corner_radius  = kwargs['_corner_radius']

    def set(self, **kwargs):
        super().set(**kwargs)
        if 'width' in kwargs:
            self.width = kwargs['width']
        if 'height' in kwargs:
            self.height = kwargs['height']
        if 'corner_radius' in kwargs:
            self.corner_radius  = kwargs['corner_radius']

    def add_leg(self, direction, position, **kwargs):
        #if 'height' not in kwargs:
        self.legs.append(Leg(self.stroke_width, self.min_length/4, **kwargs))
        #self.leg_positions.append([direction, position])

    def limits(self, rot_angle):
        diag = np.sqrt(np.square(self.width) + np.square(self.height))/2
        diag_angle = np.arctan(self.height/self.width)
        angle_sum = rot_angle + diag_angle
        angle_dif = rot_angle - diag_angle
        xmax=diag*np.max(np.abs([np.cos(angle_sum), np.cos(angle_dif)]))
        ymax=diag*np.max(np.abs([np.sin(angle_sum), np.sin(angle_dif)]))
        return [-xmax, xmax, -ymax, ymax]

    def draw(self, context):
        # Outer rectangle
        context.set_source_rgba(*self.stroke_color)
        rounded_rectangle(context, self.width, self.height, self.corner_radius)

        # Inner rectangle
        context.set_source_rgba(*self.fill_color)
        width = self.width - 2*self.stroke_width
        height = self.height - 2*self.stroke_width
        radius = self.corner_radius - self.stroke_width
        rounded_rectangle(context, width, height, radius)
