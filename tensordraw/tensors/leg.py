import numpy as np
from scipy.optimize import minimize
from scipy.optimize import shgo
from scipy.signal import argrelmin

from ..utils import distance_to_hline
from ..utils import distance_to_point
from .._drawable import Drawable

class Leg(Drawable):
    def __init__(self, parent, tip_position, **kwargs):
        self.parent = parent
        self.tip_position = tip_position

        self.width = parent.stroke_style.width
        super().__init__(**kwargs)

        if self.fill_style.default['color']:
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
    def intersections(self, res = 500, custom_path = None):
        ts = np.linspace(0,1,res)
        rot = 0
        path = self.parent.path
        if(custom_path != None):
            path = custom_path

        rot = -self.tip_position.orientation

        aux_dists = [np.linalg.norm(path(ts[i]) - path(ts[i+1])) for i,_ in enumerate(ts[:-1])]
        adjacent_dists = np.empty(res)
        adjacent_dists[0] = aux_dists[0]
        adjacent_dists[-1] = aux_dists[-1]
        adjacent_dists[1:-1] = np.max([aux_dists[:-1], aux_dists[1:]], axis = 0)

        # Compute left intersection
        origin_left = self.tipleft()
        dists_left = np.array([distance_to_hline(t, path, origin_left, rot) for t in ts])
        argmins = argrelmin(dists_left)[0]
        dists_min = dists_left[argmins]
        argmins = argmins[dists_min < adjacent_dists[argmins]]
        if(len(argmins) == 0):
            raise RuntimeError("Intersection of leg with tensor not found")
        tleft = ts[argmins[np.argmin([distance_to_point(t, path, origin_left) for t in ts[argmins]])]]

        # Compute right intersection
        origin_right = self.tipright()
        dists_right = np.array([distance_to_hline(t, path, origin_right, rot) for t in ts])
        argmins = argrelmin(dists_right)[0]
        dists_min = dists_right[argmins]
        argmins = argmins[dists_min < adjacent_dists[argmins]]
        if(len(argmins) == 0):
            raise RuntimeError("Intersection of leg with tensor not found")
        tright = ts[argmins[np.argmin([distance_to_point(t, path, origin_right) for t in ts[argmins]])]]

        return tleft, tright

    def draw(self, context):
        self.parent.path_leg_intersection(context, *self.intersections())
        context.line_to(*self.tipleft())
        context.line_to(*self.tipright())
        context.close_path()
        self.stroke_and_fill(context)
