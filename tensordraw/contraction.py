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
        self.points.append(leg1_tip - 0.01*dir_leg1) # initial point
        self.points.append(leg1_tip + dir_leg1)      # initial control point
        self.points.append(leg2_tip + dir_leg2)      # final control point
        self.points.append(leg2_tip - 0.01*dir_leg2) # final point

        if 'control_dist' in kwargs:
            dir_leg1 /= np.linalg.norm(dir_leg1)
            dir_leg2 /= np.linalg.norm(dir_leg2)
            self.points[1] = leg1_tip + kwargs['control_dist'] * dir_leg1
            self.points[2] = leg2_tip + kwargs['control_dist'] * dir_leg2

        super().__init__(**kwargs)

    def add_point(self, point, control_before = None, control_after = None):
        point = np.array(point)
        if (control_before is None) and (control_after is None):
            dist_before = np.linalg.norm(point - self.points[-4])
            dist_after = np.linalg.norm(point - self.points[-1])
            k = dist_before / (dist_before + dist_after)
            control_before = point + (1-k)*self.points[-4]/2 - \
                    k*self.points[-1]/2 
            control_after = 2*point - control_before
        elif control_before is None:
            control_before = 2*point - control_after
        elif control_after is None:
            control_after = 2*point - control_before

        self.points.insert(-2, control_before)
        self.points.insert(-2, point)
        self.points.insert(-2, control_after)

        self.fig._update_window(*self.limits())

    def cairo_path(self, context):
        context.move_to(*self.points[0])
        for i in range(1, len(self.points)-2, 3):
            context.curve_to(*self.points[i], *self.points[i+1], 
                             *self.points[i+2])

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

        #context.squarek
