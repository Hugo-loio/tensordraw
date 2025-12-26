import warnings 
from copy import deepcopy

import numpy as np

from ._base_tensor import BaseTensor
from .leg import Leg
from ..utils import Position
from ..utils import orientation
from ..utils import gradient
from ..utils import rotation

class Polygon(BaseTensor):
    def __init__(self, vertices, **kwargs):
        if(not np.allclose(vertices[-1], vertices[0])):
            vertices = np.concat((vertices, [vertices[0]]), axis = 0)
        self.vertices = np.array(vertices, dtype = float)

        x = vertices[:,0]
        y = vertices[:,1]

        self.area = 0.5 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])
        # Force vertices in clockwise direction
        if(self.area < 0):
            self.area = -self.area
            self.vertices = self.vertices[::-1]
            x = self.vertices[:,0]
            y = self.vertices[:,1]

        # Side i in between vertex i and i+1
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

        cx = np.sum((x[:-1] + x[1:])*(x[:-1]*y[1:] - x[1:]*y[:-1]))/(6*self.area)
        cy = np.sum((y[:-1] + y[1:])*(x[:-1]*y[1:] - x[1:]*y[:-1]))/(6*self.area)
        # Shift origin to the centroid
        if kwargs.get('center', True):
            self.vertices -= np.array([cx,cy])

        self.min_length = np.min(self.side_lengths)
        self.diffs = diffs
        self.diffs_dir = diffs/np.linalg.norm(diffs, axis = 1)[:,np.newaxis]

        self.corner_width = self.min_length/10

        super().__init__(**kwargs)

        if self.stroke_style.default['width']:
            self.stroke_style.set(width = self.min_length/10)

        if 'corner_width' not in kwargs:
            #self.corner_width =  self.min_length/10
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
            self._compute_rounded_corners()

    #def perimeter(self):
    #    return 2*np.pi*self.radius

    def add_leg(self, side, side_pos = 0.5, tilt = 0, **kwargs):
        h = 1E-5*self.side_lengths[side]
        t = (side + side_pos)/self.nsides
        # Rotate gradient -90 degrees + tilt for the leg direction
        grad = gradient(self.path, t, h)
        perp_dir = rotation(-np.pi/2 + tilt) @ grad/np.linalg.norm(grad) 
        angle = orientation(perp_dir)

        if 'length' in kwargs:
            length = kwargs['length'] 
        else:
            length = self.min_length/3

        tip_position = Position(*(self.path(t) + perp_dir*length), angle)
        self.legs.append(Leg(self, tip_position, self.path(t), **kwargs))

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
        elif(t <= 1 - delta):
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


    def limits(self, R):
        points = np.array([R @ self.path(t) for t in np.linspace(0,1,200*self.nsides)])
        xmin = np.min(points[:,0]) - self.stroke_style.width/2
        xmax = np.max(points[:,0]) + self.stroke_style.width/2
        ymin = np.min(points[:,1]) - self.stroke_style.width/2
        ymax = np.max(points[:,1]) + self.stroke_style.width/2
        if(self.corner_width == 0):
            for i in np.arange(self.nsides)[np.logical_not(self.obtuse)]:
                vertex_dir = rotation(-np.pi/2) @ (self.diffs_dir[i-1] + self.diffs_dir[i])
                vertex_dir = vertex_dir/np.linalg.norm(vertex_dir)
                h = self.stroke_style.width/np.sin(self.angles[i]/2)
                x,y = self.vertices[i] + h*vertex_dir/2
                xmin = np.min([xmin, x])
                xmax = np.max([xmax, x])
                ymin = np.min([ymin, y])
                ymax = np.max([ymax, y])
        return self.leg_limtis(xmin, xmax, ymin, ymax, R)

    def _path_rounded_corner(self, context, index, start_angle, end_angle):
        if(self.obtuse[index]):
            context.arc_negative(*self.corner_centers[index], 
                                 self.corner_radii[index], 
                                 start_angle, 
                                 end_angle)
        else:
            context.arc(*self.corner_centers[index],
                        self.corner_radii[index], 
                        start_angle, 
                        end_angle)

    def draw(self, context):
        ### Polygon with rounded corners
        context.move_to(*self.corner_starts[0])
        for i,v in enumerate(self.vertices[:-1]):
            context.line_to(*self.corner_starts[i])
            self._path_rounded_corner(context, i, self.corner_start_angles[i], self.corner_end_angles[i])
        context.close_path()

        self.stroke_and_fill(context)

        for leg in self.legs:
            leg.draw(context)

    '''
    TODO: improove the leg intersection drawing
    For now we have something that works, leave this for later

    def _path_segment(self, context, side_number, segment, tstart = 0, tend = 1):
        match segment:
            case 0:
                angle_t0 = self.corner_mid_angles[side_number]
                angle_t1 = self.corner_end_angles[side_number]
                start_angle = angle_t0 + tstart*(angle_t1 - angle_t0)
                end_angle = angle_t0 + tend*(angle_t1 - angle_t0)
                self._path_rounded_corner(context, side_number, start_angle, end_angle)
            case 1:
                point_t0 = self.corner_ends[side_number]
                point_t1 = self.corner_starts[(side_number + 1) % self.nsides]
                start_point = point_t0 + tstart*(point_t1 - point_t0)
                end_point = point_t0 + tend*(point_t1 - point_t0)
                context.line_to(*end_point)
            case 2:
                index = (side_number + 1) % self.nsides
                angle_t0 = self.corner_start_angles[index]
                angle_t1 = self.corner_mid_angles[index]
                start_angle = angle_t0 + tstart*(angle_t1 - angle_t0)
                end_angle = angle_t0 + tend*(angle_t1 - angle_t0)
                self._path_rounded_corner(context, side_number, start_angle, end_angle)

    def path_leg_intersection(self, context, tleft, tright):
        self.easy_path_leg_intersection(context, tleft, tright)
        ts = np.array([tright, tleft])*self.nsides
        side_numbers = (ts).astype(int)
        side_numbers[side_numbers == self.nsides] -= 1
        ts -= side_numbers
        deltas = self.corner_width/self.side_lengths[side_numbers]
        segments = np.logical_and(ts > deltas, ts <= 1 - deltas)*1 + (ts > 1 - deltas)*2 

        for i in range(2):
            match segments[i]:
                case 0:
                    ts[i] = ts[i]/deltas[i]
                case 1:
                    ts[i] = (ts[i] - deltas[i])/(1-2*deltas[i])
                case 2:
                    ts[i] = (ts[i] - (1-deltas[i]))/deltas[i]

        context.move_to(*self.path(ts[0], side_numbers[0]))

        side_segment_stop = np.array([side_numbers[0], segments[0], 0])
        count = 0
        while(side_segment_stop[-1] == 0):
            tstart = 0 + (count == 0)*ts[0]
            tend = 1
            if(side_segment_stop[0] == side_numbers[1] and side_segment_stop[1] == segments[1]):
                tend = ts[1]
                side_segment_stop[-1] = 1

            self._path_segment(context, *side_segment_stop[0:1], tstart, tend)

            side_segment_stop[1] = (side_segment_stop[1] + 1) % 3
            if(side_segment_stop[1] == 0):
                side_segment_stop[0] += 1 
            count += 1
            '''
