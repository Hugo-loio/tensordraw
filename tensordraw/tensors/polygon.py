import numpy as np

from ._base_tensor import BaseTensor
from .leg import Leg
from ..utils import Position
from ..utils import rotation

class Polygon(BaseTensor):
    def __init__(self, vertices, **kwargs):
        super().__init__(**kwargs)

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

        self.angles = np.arccos(-np.einsum("ij,ij->i", diffs[1:], diffs[:-1])/(self.side_lengths[1:]*self.side_lengths[:-1]))
        last_angle = np.arccos(-np.dot(diffs[0], diffs[-1])/(self.side_lengths[0]*self.side_lengths[-1]))
        self.angles = np.concat((self.angles, [last_angle]), axis = 0) 

        self.convex = np.cross(diffs[:-1], diffs[1:]) < 0
        self.convex = np.concat((self.convex, [np.cross(diffs[-1], diffs[0]) < 0]), axis = 0)
        self.angles[self.convex] = 2*np.pi  - self.angles[self.convex]

        if(np.sum(self.angles) != (len(self.side_lengths)-2)*np.pi):
            raise ValueError("The internal angles of the polygon do not properly add up")

        # Shift origin to the centroid
        cx = np.sum((x[:-1] + x[1:])*(x[:-1]*y[1:] - x[1:]*y[:-1]))/(6*self.area)
        cy = np.sum((y[:-1] + y[1:])*(x[:-1]*y[1:] - x[1:]*y[:-1]))/(6*self.area)
        self.vertices -= np.array([cx,cy])

        self.min_length = np.min(self.side_lengths)
        if 'stroke_width' not in kwargs:
            self.stroke_width = self.min_length/10

        if 'corner_width' in kwargs:
            self.corner_width  = kwargs['corner_width']

    def set(self, **kwargs):
        super().set(**kwargs)

    def perimeter(self):
        return 2*np.pi*self.radius

    def add_leg(self, angle, tilt = 0, **kwargs):
        return 0

    def path(self, t):
        return 0

    def limits(self, R):
        rotated_vertices = np.einsum("jk,ik", R, self.vertices)
        x = rotated_vertices[:,0]
        y = rotated_vertices[:,1]
        xmin = np.min(x)
        xmax = np.max(x)
        ymin = np.min(y)
        ymax = np.max(y)
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
        # Outer polygon (TODO: inner transparency)
        context.set_source_rgba(*self.stroke_color)
        context.move_to(*self.vertices[0])
        [context.line_to(*v) for v in self.vertices[:-1]]
        context.close_path()
        context.fill()

        return 0
        # Polygon circle
        context.set_source_rgba(*self.fill_color)
        context.fill()

        #for leg in self.legs:
        #    self.draw_leg(leg, context)
