import numpy as np
import cairo

from ._drawable import Drawable

class Contraction(Drawable):
    def __init__(self, fig, leg1_base, leg1_tip, 
                 leg2_tip, leg2_base, **kwargs):
        self.fig = fig

        dir_leg1 = leg1_tip - leg1_base
        dir_leg2 = leg2_tip - leg2_base

        self.points = []
        self.points.append(leg1_base + 0.9*dir_leg1) # initial straight point
        self.points.append(leg1_tip)                 # initial curve point
        self.points.append(leg1_tip + dir_leg1)      # initial control point
        self.points.append(leg2_tip + dir_leg2)      # final control point
        self.points.append(leg2_tip)                 # final curve point
        self.points.append(leg2_base + 0.9*dir_leg2) # final straight point

        if 'handle_lengths' in kwargs:
            dir_leg1 /= np.linalg.norm(dir_leg1)
            dir_leg2 /= np.linalg.norm(dir_leg2)
            self.points[2] = leg1_tip + kwargs['handle_lengths'][0] * dir_leg1
            self.points[3] = leg2_tip + kwargs['handle_lengths'][1] * dir_leg2

        super().__init__(**kwargs)

    def add_point(self, point, control_before = None, 
                  control_after = None, **kwargs):
        point = np.array(point)
        if (control_before is None) and (control_after is None):
            dist_before = np.linalg.norm(point - self.points[-5])
            dist_after = np.linalg.norm(point - self.points[-2])
            k = dist_before / (dist_before + dist_after)
            control_before = point + (1-k)*self.points[-5]/2 - \
                    k*self.points[-2]/2 
            control_after = 2*point - control_before
        elif control_before is None:
            control_before = 2*point - control_after
        elif control_after is None:
            control_after = 2*point - control_before

        if 'handle_lengths' in kwargs:
            k = kwargs['handle_lengths'][0]/np.linalg.norm(point-control_before)
            control_before = k * (control_before - point) + point
            k = kwargs['handle_lengths'][1]/np.linalg.norm(point-control_after)
            control_after = k * (control_after - point) + point

        self.points.insert(-3, control_before)
        self.points.insert(-3, point)
        self.points.insert(-3, control_after)

        self.fig._update_window(*self.limits())

    def cairo_path(self, context):
        context.move_to(*self.points[0])
        context.line_to(*self.points[1])
        for i in range(2, len(self.points)-3, 3):
            context.curve_to(*self.points[i], *self.points[i+1], 
                             *self.points[i+2])
        context.line_to(*self.points[-1])

    def limits(self):
        surface = cairo.ImageSurface(cairo.FORMAT_A8, 0, 0)
        context = cairo.Context(surface)

        self.cairo_path(context)
        
        xmin, ymin, xmax, ymax = context.path_extents()
        sw = self.stroke_style.width
        return [xmin-sw/2, xmax+sw/2, ymin-sw/2, ymax+sw/2]

    def draw(self, context):
        self.cairo_path(context)
        self.stroke_style.stroke(context)
