import numpy as np
from scipy.signal import argrelmin

from .utils import distance_to_hline
from .utils import distance_to_point
from .utils import path_line_intersection
from ._drawable import Drawable

class Leg(Drawable):
    def __init__(self, parent, tip_position, base_point, res = 1000, **kwargs):
        self.parent = parent
        self.tip_position = tip_position
        self.base_point = base_point 
        self.width = parent.stroke_style.width

        super().__init__(**kwargs)

        self.intersections = self._compute_intersections(res)

        if self.fill_style.default['_color']:
            self.fill_style.set(color = parent.stroke_style.color)
        if self.stroke_style.default['width']:
            self.stroke_style.set(width = 0)

    def tipleft(self):
        x = self.tip_position.x - np.sin(self.tip_position.orientation)*self.width/2
        y = self.tip_position.y + np.cos(self.tip_position.orientation)*self.width/2
        return np.array([x,y])

    def tipright(self):
        x = self.tip_position.x + np.sin(self.tip_position.orientation)*self.width/2
        y = self.tip_position.y - np.cos(self.tip_position.orientation)*self.width/2
        return np.array([x,y])

    # Find the intersection between the leg's boundaries and the parent tensor path
    def _compute_intersections(self, res, custom_path = None):
        path = self.parent.path
        if(custom_path != None):
            path = custom_path
        inclination = self.tip_position.orientation

        ts_left = path_line_intersection(path, self.tipleft(), inclination, res)
        tleft = ts_left[np.argmin(
            [distance_to_point(t, path, self.base_point) for t in ts_left])]

        ts_right = path_line_intersection(path, self.tipright(), inclination, res)
        tright = ts_right[np.argmin(
            [distance_to_point(t, path, self.base_point) for t in ts_right])]
        return tleft, tright

    '''
        TODO: a better minimization method to improve resolution and speed
        If there are simple equations for each of the path segments of the tensors then the intersection points could be found analytically
        For now we have something that works so let's leave this for later
    '''

    def draw(self, context):
        self.parent.path_leg_intersection(context, *self.intersections)
        context.line_to(*self.tipleft())
        context.line_to(*self.tipright())
        context.close_path()
        self.stroke_and_fill(context)
