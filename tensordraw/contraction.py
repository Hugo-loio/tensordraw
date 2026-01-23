import numpy as np
import cairo

from ._drawable import Drawable

class Contraction(Drawable):
    def __init__(self, fig, leg1_base, leg1_tip, 
                 leg2_tip, leg2_base, **kwargs):
        self.fig = fig

        leg1_disp = leg1_tip - leg1_base
        leg2_disp = leg2_tip - leg2_base
        leg1_len  = np.linalg.norm(leg1_disp)
        leg2_len  = np.linalg.norm(leg2_disp)
        leg1_dir  = leg1_disp / leg1_len
        leg2_dir  = leg2_disp / leg2_len
        tip_dist  = np.linalg.norm(leg1_tip - leg2_tip)

        k1 = np.max([leg1_len, tip_dist*(2/5)])
        k2 = np.max([leg2_len, tip_dist*(2/5)])

        self.points = []
        self.points.append(leg1_base + 0.9*leg1_disp) # initial straight point
        self.points.append(leg1_tip)                  # initial curve point
        self.points.append(leg1_tip + k1 * leg1_dir)  # initial control point
        self.points.append(leg2_tip + k2 * leg2_dir)  # final control point
        self.points.append(leg2_tip)                  # final curve point
        self.points.append(leg2_base + 0.9*leg2_disp) # final straight point

        if 'handle_lengths' in kwargs:
            self.points[2] = leg1_tip + kwargs['handle_lengths'][0] * leg1_dir
            self.points[3] = leg2_tip + kwargs['handle_lengths'][1] * leg2_dir

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
