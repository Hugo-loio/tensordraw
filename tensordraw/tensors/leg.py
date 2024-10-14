import numpy as np
from scipy.optimize import minimize
from scipy.optimize import shgo
from scipy.signal import argrelmin

from ..utils import distance_to_hline
from ..utils import distance_to_point

class Leg():
    def __init__(self, parent, tip_position, **kwargs):
        self.parent = parent
        self.tip_position = tip_position

        self.width = parent.stroke_width
        self.color = parent.stroke_color
        self.set(**kwargs)

    def set(self, **kwargs):
        if 'width' in kwargs:
            self.width = kwargs['width']
        if 'color' in kwargs:
            self.color = kwargs['color']

    def tipleft(self):
        x = self.tip_position.x - np.sin(self.tip_position.orientation)*self.width/2
        y = self.tip_position.y + np.cos(self.tip_position.orientation)*self.width/2
        return np.array([x,y])

    def tipright(self):
        x = self.tip_position.x + np.sin(self.tip_position.orientation)*self.width/2
        y = self.tip_position.y - np.cos(self.tip_position.orientation)*self.width/2
        return np.array([x,y])

    # Find the intersection between the leg's boundaries and the parent tensor path
    def intersections(self, res = 500, custom_path = None):
        ts = np.linspace(0,1,res)
        perimeter = self.parent.perimeter()
        rot = 0
        path = self.parent.path
        if(custom_path != None):
            path = custom_path

        rot = -self.tip_position.orientation
        max_dist = perimeter/res

        # Compute left intersection
        origin_left = self.tipleft()
        dists_left = np.array([distance_to_hline(t, path, origin_left, rot) for t in ts])
        argmins = argrelmin(dists_left)[0]
        dists_min = dists_left[argmins]
        argmins = argmins[dists_min < max_dist]
        if(len(argmins) == 0):
            raise RuntimeError("Intersection of leg with tensor not found")
        tleft = ts[argmins[np.argmin([distance_to_point(t, path, origin_left) for t in ts[argmins]])]]

        # Compute right intersection
        origin_right = self.tipright()
        dists_right = np.array([distance_to_hline(t, path, origin_right, rot) for t in ts])
        argmins = argrelmin(dists_right)[0]
        dists_min = dists_right[argmins]
        argmins = argmins[dists_min < max_dist]
        if(len(argmins) == 0):
            raise RuntimeError("Intersection of leg with tensor not found")
        tright = ts[argmins[np.argmin([distance_to_point(t, path, origin_right) for t in ts[argmins]])]]

        return tleft, tright
