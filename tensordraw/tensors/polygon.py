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

        if 'stroke_width' not in kwargs:
            self.stroke_width = self.min_length/10

        self.corner_width =  self.min_length/10
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

    def _perp_dir(self, i):
        aux_mat = np.array([[0,1],[-1,0]])
        diff_sum = self.diffs[i]/np.linalg.norm(self.diffs[i]) + \
                self.diffs[i-1]/np.linalg.norm(self.diffs[i-1])
        perp_dir = aux_mat @ diff_sum
        return perp_dir/np.linalg.norm(perp_dir)


    def draw(self, context):
        # Compute inner vertices
        aux_mat = np.array([[0,-1],[1,0]])
        n = len(self.vertices) - 1
        perp_dir = [self._perp_dir(i) for i in range(n)]
        h = [self.stroke_width/np.sin(self.angles[i]/2) for i in range(n)]
        inner_vertices = [v - h[i]*perp_dir[i] for i,v in enumerate(self.vertices[:-1])]
        inner_vertices.append(inner_vertices[0])

        # Outer polygon with rounded corners
        context.set_source_rgba(*self.stroke_color)
        context.move_to(*self.vertices[0] - self.diffs_dir[-1]*self.corner_width)
        for i,v in enumerate(self.vertices[:-1]):
            left = v - self.diffs_dir[i-1]*self.corner_width
            right = v + self.diffs_dir[i]*self.corner_width
            radius = abs(self.corner_width*np.tan(self.angles[i]/2))

            perp_right_dir = np.array([-self.diffs_dir[i,1], self.diffs_dir[i,0]])
            if(self.obtuse[i]):
                perp_right_dir = -perp_right_dir
            center = right + perp_right_dir*radius

            end_angle = orientation(-perp_right_dir)
            angle = np.pi - self.angles[i]
            context.line_to(*left)
            if(self.obtuse[i]):
                context.arc_negative(*center, radius, end_angle - angle, end_angle)
            else:
                context.arc(*center, radius, end_angle - angle, end_angle)

        context.close_path()

        inner_enum = [(i,v) for i,v in enumerate(inner_vertices[:-1])]
        i,v = inner_enum[-1]
        context.move_to(*v + self.diffs_dir[i]*self.corner_width)
        for i,v in inner_enum[::-1]:
            left = v - self.diffs_dir[i-1]*self.corner_width
            right = v + self.diffs_dir[i]*self.corner_width
            radius = abs(self.corner_width*np.tan(self.angles[i]/2))

            perp_right_dir = np.array([-self.diffs_dir[i,1], self.diffs_dir[i,0]])
            if(self.obtuse[i]):
                perp_right_dir = -perp_right_dir
            center = right + perp_right_dir*radius

            end_angle = orientation(-perp_right_dir)
            angle = np.pi - self.angles[i]
            if(self.obtuse[i]):
                context.arc(*center, radius, end_angle, end_angle - angle)
            else:
                context.arc_negative(*center, radius, end_angle, end_angle - angle)

            context.line_to(*right)
            context.line_to(*left)

        #[context.line_to(*v) for v in inner_vertices[::-1]]
        context.close_path()
        context.fill()

        # Polygon circle

        #for leg in self.legs:
        #    self.draw_leg(leg, context)
