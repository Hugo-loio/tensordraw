import numpy as np

from ._base_tensor import BaseTensor
from .leg import Leg
from ..utils import Position
from ..utils import rotation
from ..utils import orientation

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
        first_angle = np.arccos(-np.dot(diffs[0], diffs[-1])/(self.side_lengths[0]*self.side_lengths[-1]))
        self.angles = np.concat(([first_angle], self.angles), axis = 0) 

        self.obtuse = np.cross(diffs[:-1], diffs[1:]) < 0
        self.obtuse = np.concat(([np.cross(diffs[-1], diffs[0]) < 0], self.obtuse), axis = 0)
        self.angles[self.obtuse] = 2*np.pi  - self.angles[self.obtuse]

        if(np.abs(np.sum(self.angles) - (len(self.side_lengths)-2)*np.pi) > 1E-8):
            raise ValueError("The internal angles of the polygon do not properly add up")

        # Shift origin to the centroid
        cx = np.sum((x[:-1] + x[1:])*(x[:-1]*y[1:] - x[1:]*y[:-1]))/(6*self.area)
        cy = np.sum((y[:-1] + y[1:])*(x[:-1]*y[1:] - x[1:]*y[:-1]))/(6*self.area)
        self.vertices -= np.array([cx,cy])

        self.min_length = np.min(self.side_lengths)
        self.diffs = diffs
        self.diffs_dir = diffs/np.linalg.norm(diffs, axis = 1)[:,np.newaxis]

        if 'stroke_style' not in kwargs:
            self.stroke_style.width = self.min_length/10

        self.corner_width =  self.min_length/10
        if 'corner_width' in kwargs:
            self.corner_width = kwargs['corner_width']

    def set(self, **kwargs):
        super().set(**kwargs)
        if 'corner_width' in kwargs:
            self.corner_width = kwargs['corner_width']

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
        # TODO: These limits need to be fixed!
        # Maybe we can just use a parent function that uses the discretized path
        xmin = np.min(x) - self.stroke_style.width/2
        xmax = np.max(x) + self.stroke_style.width/2
        ymin = np.min(y) - self.stroke_style.width/2
        ymax = np.max(y) + self.stroke_style.width/2
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

    def _perp_dir(self, i):
        aux_mat = np.array([[0,1],[-1,0]])
        diff_sum = self.diffs[i]/np.linalg.norm(self.diffs[i]) + \
                self.diffs[i-1]/np.linalg.norm(self.diffs[i-1])
        perp_dir = aux_mat @ diff_sum
        return perp_dir/np.linalg.norm(perp_dir)


    def draw(self, context):
        ### Compute auxiliary variables
        aux_mat = np.array([[0,-1],[1,0]])
        n = len(self.vertices) - 1
        perp_dir = [self._perp_dir(i) for i in range(n)]
        # Radii of the rounded corners
        radii = np.abs(self.corner_width*np.tan(self.angles/2))
        # Auxiliary points and directions
        perp_right_dir = self.diffs_dir @ np.array([[0,1],[-1,0]])
        perp_right_dir[self.obtuse] = -perp_right_dir[self.obtuse]
        right = self.vertices[:-1] + self.diffs_dir*self.corner_width
        # Centers of the rounded corners
        centers = right + perp_right_dir*radii[:,np.newaxis]
        # Start and end angle of the rounded corners
        end_angles = [orientation(-direction) for direction in perp_right_dir]
        start_angles = end_angles + self.angles - np.pi

        ### Polygon with rounded corners
        context.move_to(*self.vertices[0] - self.diffs_dir[-1]*self.corner_width)
        for i,v in enumerate(self.vertices[:-1]):
            left = v - self.diffs_dir[i-1]*self.corner_width
            context.line_to(*left)
            if(self.obtuse[i]):
                context.arc_negative(*centers[i], radii[i], start_angles[i], end_angles[i])
            else:
                context.arc(*centers[i], radii[i], start_angles[i], end_angles[i])
        context.close_path()

        self.fill_style.fill_preserve(context)
        self.stroke_style.stroke(context)

        #for leg in self.legs:
        #    self.draw_leg(leg, context)
