import warnings 
from copy import deepcopy

import numpy as np

from ._base_tensor import BaseTensor
from .leg import Leg
from ..utils import Position
from ..utils import rotation
from ..utils import orientation

class Polygon(BaseTensor):
    def __init__(self, vertices, **kwargs):
        if(not np.allclose(vertices[-1], vertices[0])):
            vertices = np.concat((vertices, [vertices[0]]), axis = 0)
        self.vertices = np.array(vertices, dtype = float)

        x = vertices[:,0]
        y = vertices[:,1]

        self.area = 0.5 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])
        # Correct vertices in clockwise direction
        if(self.area < 0):
            self.area = -self.area
            self.vertices = self.vertices[::-1]
            x = self.vertices[:,0]
            y = self.vertices[:,1]

        diffs = self.vertices[1:] - self.vertices[:-1]

        self.side_lengths = np.linalg.norm(diffs, axis = 1)
        self.nsides = len(self.side_lengths)

        self.angles = np.arccos(-np.einsum("ij,ij->i", diffs[1:], diffs[:-1])/(self.side_lengths[1:]*self.side_lengths[:-1]))
        first_angle = np.arccos(-np.dot(diffs[0], diffs[-1])/(self.side_lengths[0]*self.side_lengths[-1]))
        self.angles = np.concat(([first_angle], self.angles), axis = 0) 

        self.obtuse = np.cross(diffs[:-1], diffs[1:]) < 0
        self.obtuse = np.concat(([np.cross(diffs[-1], diffs[0]) < 0], self.obtuse), axis = 0)
        self.angles[self.obtuse] = 2*np.pi  - self.angles[self.obtuse]

        if(np.abs(np.sum(self.angles) - (self.nsides-2)*np.pi) > 1E-8):
            raise ValueError("The internal angles of the polygon do not properly add up")

        # Shift origin to the centroid
        cx = np.sum((x[:-1] + x[1:])*(x[:-1]*y[1:] - x[1:]*y[:-1]))/(6*self.area)
        cy = np.sum((y[:-1] + y[1:])*(x[:-1]*y[1:] - x[1:]*y[:-1]))/(6*self.area)
        self.vertices -= np.array([cx,cy])

        self.min_length = np.min(self.side_lengths)
        self.diffs = diffs
        self.diffs_dir = diffs/np.linalg.norm(diffs, axis = 1)[:,np.newaxis]

        super().__init__(**kwargs)

        if self.stroke_style.default['width']:
            self.stroke_style.set(width = self.min_length/10)

        if 'corner_width' not in kwargs:
            self.corner_width =  self.min_length/10
            self._compute_rounded_corners()


    def _compute_rounded_corners(self):
        if(self.corner_width > self.min_length/2):
            warnings.warn("Corner width cannot be larger than half the length of the smallest size of the polygon", UserWarning)
            self.corner_width = self.min_length/2
        # Auxiliary directions
        perp_right_dir = self.diffs_dir @ np.array([[0,1],[-1,0]])
        perp_right_dir[self.obtuse] = -perp_right_dir[self.obtuse]
        # Radii of the rounded corners
        self.corner_radii = np.abs(self.corner_width*np.tan(self.angles/2))
        # Rounded corner start and end points
        self.corner_ends = self.vertices[:-1] + self.diffs_dir*self.corner_width 
        self.corner_starts = self.vertices[:-1] - np.roll(self.diffs_dir, 1, axis = 0)*self.corner_width 
        # Centers of the rounded corners
        self.corner_centers = self.corner_ends + perp_right_dir*self.corner_radii[:,np.newaxis]
        # Angles of the rounded corners
        self.corner_end_angles = [orientation(-direction) for direction in perp_right_dir]
        self.corner_start_angles = self.corner_end_angles + self.angles - np.pi
        self.corner_mid_angles = (self.corner_start_angles + self.corner_end_angles)/2

    def set(self, **kwargs):
        super().set(**kwargs)
        if 'corner_width' in kwargs:
            self.corner_width = kwargs['corner_width']
            self._compute_rounded_corners()

    def perimeter(self):
        return 2*np.pi*self.radius

    def add_leg(self, angle, tilt = 0, **kwargs):
        return 0

    def path(self, t, side_number = -1):
        # Side i in between vertex i and i+1
        if(side_number < 0):
            side_number = int(t*self.nsides)
            if(side_number == self.nsides):
                side_number -= 1
            t = t*self.nsides - side_number
        delta = self.corner_width/self.side_lengths[side_number]
        if(t < delta):
            t = t/delta
            angle_t0 = self.corner_mid_angles[side_number]
            angle_t1 = self.corner_end_angles[side_number]
            angle = angle_t0 + t*(angle_t1 - angle_t0)
            r = self.corner_radii[side_number]
            c = self.corner_centers[side_number]
            return c + r*np.array([np.cos(angle), np.sin(angle)])
        elif(t < 1 - delta):
            t = (t - delta)/(1 - 2*delta)
            point_t0 = self.corner_ends[side_number]
            point_t1 = self.corner_starts[(side_number + 1) % self.nsides]
            return point_t0 + t*(point_t1 - point_t0)
        else:
            t = (t - (1 - delta))/delta
            index = (side_number + 1) % self.nsides
            angle_t0 = self.corner_start_angles[index]
            angle_t1 = self.corner_mid_angles[index]
            angle = angle_t0 + t*(angle_t1 - angle_t0)
            r = self.corner_radii[index]
            c = self.corner_centers[index]
            return c + r*np.array([np.cos(angle), np.sin(angle)])

    #def perimeter(self):

    def limits(self, R):
        points = np.array([R @ self.path(t) for t in np.linspace(0,1,200*self.nsides)])
        xmin = np.min(points[:,0]) - self.stroke_style.width/2
        xmax = np.max(points[:,0]) + self.stroke_style.width/2
        ymin = np.min(points[:,1]) - self.stroke_style.width/2
        ymax = np.max(points[:,1]) + self.stroke_style.width/2
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

    # This function was used for testing the path function
    def draw_from_path(self, context):
        ss = deepcopy(self.stroke_style)
        ss.set(color = (0,1,0,1), width = ss.width/4)
        points = [self.path(t) for t in np.linspace(0,1,200*self.nsides)]
        context.move_to(*points[0])
        for point in points:
            context.line_to(*point)
        context.close_path()
        ss.stroke(context)

    def draw(self, context):
        ### Polygon with rounded corners
        context.move_to(*self.corner_starts[0])
        for i,v in enumerate(self.vertices[:-1]):
            context.line_to(*self.corner_starts[i])
            if(self.obtuse[i]):
                context.arc_negative(*self.corner_centers[i], 
                                     self.corner_radii[i], 
                                     self.corner_start_angles[i], 
                                     self.corner_end_angles[i])
            else:
                context.arc(*self.corner_centers[i], 
                            self.corner_radii[i], 
                            self.corner_start_angles[i], 
                            self.corner_end_angles[i])
        context.close_path()

        self.fill_style.fill_preserve(context)
        self.stroke_style.stroke(context)

        #for leg in self.legs:
        #    self.draw_leg(leg, context)
