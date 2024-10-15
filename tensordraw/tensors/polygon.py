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
        ### Compute auxilary variables
        aux_mat = np.array([[0,-1],[1,0]])
        n = len(self.vertices) - 1
        perp_dir = [self._perp_dir(i) for i in range(n)]
        h = np.abs(self.stroke_width/np.sin(self.angles/2))
        inner_vertices = [v - h[i]*perp_dir[i] for i,v in enumerate(self.vertices[:-1])]
        inner_vertices.append(inner_vertices[0])
        # Raddi of the inner and outer rounded corners
        outer_radii = np.abs(self.corner_width*np.tan(self.angles/2))
        inner_radii = outer_radii - self.stroke_width
        inner_radii[self.obtuse] += 2*self.stroke_width
        no_inner_round = inner_radii <= 0
        inner_radii[no_inner_round] = 0
        # Inner corner width
        inner_corner_width = np.repeat(0.0, n)
        indices_accute = np.logical_not(np.logical_or(self.obtuse,no_inner_round))
        inner_corner_width[indices_accute] = self.corner_width - np.sqrt(np.square(h[indices_accute]) - np.square(self.stroke_width))
        indices_obtuse = np.logical_and(self.obtuse,np.logical_not(no_inner_round))
        inner_corner_width[indices_obtuse] = self.corner_width + np.sqrt(np.square(h[indices_obtuse]) - np.square(self.stroke_width))
        # Auxilary points and directions
        perp_right_dir = self.diffs_dir @ np.array([[0,1],[-1,0]])
        perp_right_dir[self.obtuse] = -perp_right_dir[self.obtuse]
        right = self.vertices[:-1] + self.diffs_dir*self.corner_width
        # Centers of the rounded corners
        centers = right + perp_right_dir*outer_radii[:,np.newaxis]
        # Start and end angle of the rounded corners
        end_angles = [orientation(-direction) for direction in perp_right_dir]
        start_angles = end_angles + self.angles - np.pi

        ### Outer polygon with rounded corners
        context.set_source_rgba(*self.stroke_color)
        context.move_to(*self.vertices[0] - self.diffs_dir[-1]*self.corner_width)
        for i,v in enumerate(self.vertices[:-1]):
            left = v - self.diffs_dir[i-1]*self.corner_width
            context.line_to(*left)
            if(self.obtuse[i]):
                context.arc_negative(*centers[i], outer_radii[i], start_angles[i], end_angles[i])
            else:
                context.arc(*centers[i], outer_radii[i], start_angles[i], end_angles[i])
        context.close_path()

        ### Inner polygon in opposite direction to fill the stroke section
        inner_enum = [(i,v) for i,v in enumerate(inner_vertices[:-1])]
        i,v = inner_enum[-1]
        context.move_to(*v + self.diffs_dir[i]*self.corner_width)
        for i,v in inner_enum[::-1]:
            right = v + self.diffs_dir[i]*inner_corner_width[i]
            context.line_to(*right)
            if(self.obtuse[i]):
                context.arc(*centers[i], inner_radii[i], end_angles[i], start_angles[i])
            else:
                context.arc_negative(*centers[i], inner_radii[i], end_angles[i], start_angles[i])
        context.close_path()
        context.fill()

        ### Inner polygon to fill inside
        context.set_source_rgba(*self.fill_color)
        i,v = inner_enum[0]
        context.move_to(*v - self.diffs_dir[i-1]*self.corner_width)
        for i,v in inner_enum:
            left = v - self.diffs_dir[i-1]*inner_corner_width[i]
            context.line_to(*left)
            if(self.obtuse[i]):
                context.arc_negative(*centers[i], inner_radii[i], start_angles[i], end_angles[i])
            else:
                context.arc(*centers[i], inner_radii[i], start_angles[i], end_angles[i])
        context.close_path()
        context.fill()

        #[context.line_to(*v) for v in inner_vertices[::-1]]

        # Polygon circle

        #for leg in self.legs:
        #    self.draw_leg(leg, context)
