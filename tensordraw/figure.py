import os
from copy import deepcopy

import cairo
import numpy as np

from .utils import Position
from .utils import pos_to_point
from .utils import rotation
from .utils import orientation
from .utils import path_line_intersection
from .utils import distance_to_point
from .contraction import Contraction
from .leg import Leg
from ._placeable import Placeable

class Figure():
    def __init__(self):
        self.objects = []
        self.positions = []
        self.contractions = []
        # Window limits [xmin, xmax, ymin, ymax]
        self.window = []

    def place(self, obj : Placeable, x, y, orientation = 0):
        self.objects.append(deepcopy(obj))
        self.positions.append(Position(x, y, orientation))

        R = rotation(orientation)
        limits = obj.limits(R)
        xmin = x + limits[0]
        xmax = x + limits[1]
        ymin = y + limits[2]
        ymax = y + limits[3]
        if(len(self.window) == 0):
            self.window = np.array([xmin, xmax, ymin, ymax])
        else:
            self._update_window(xmin, xmax, ymin, ymax)

        return len(self.objects) - 1

    def _contract_legs(self, tensor1_idx, leg1_idx, tensor2_idx, leg2_idx, 
                       **kwargs):
        leg1 = self.objects[tensor1_idx].legs[leg1_idx]
        R1 = rotation(self.positions[tensor1_idx].orientation)
        p1 = pos_to_point(self.positions[tensor1_idx])
        leg1_base = p1 + R1 @ leg1.base_point
        leg1_tip = p1 + R1 @ pos_to_point(leg1.tip_position)

        leg2 = self.objects[tensor2_idx].legs[leg2_idx]
        R2 = rotation(self.positions[tensor2_idx].orientation)
        p2 = pos_to_point(self.positions[tensor2_idx])
        leg2_base = p2 + R2 @ leg2.base_point
        leg2_tip = p2 + R2 @ pos_to_point(leg2.tip_position)

        if not (('sw' in kwargs) or ('strokewidth' in kwargs)):
            kwargs['strokewidth'] = np.max([leg1.width, leg2.width])

        self.contractions.append(Contraction(self, leg1_base, leg1_tip, 
                                             leg2_tip, leg2_base, **kwargs))

        self._update_window(*self.contractions[-1].limits())
        return self.contractions[-1]

    def _contract_tensors(self, tensor1_idx, tensor2_idx, **kwargs):
        tensor1 = self.objects[tensor1_idx]
        path1 = tensor1.path
        shift1 = pos_to_point(self.positions[tensor1_idx])
        centroid1 = shift1 + tensor1.centroid
        tensor2 = self.objects[tensor2_idx]
        path2 = tensor2.path
        shift2 = pos_to_point(self.positions[tensor2_idx])
        centroid2 = shift2 + tensor2.centroid

        disp12 = centroid2 - centroid1
        inclination = orientation(disp12)
        origin = (centroid1 + centroid2)/2
        origin1 = origin - shift1 
        origin2 = origin - shift2 
        res = kwargs.get('res', 1000)

        ts1 = path_line_intersection(path1, origin1, inclination, res)
        ts2 = path_line_intersection(path2, origin2, inclination, res)
        t1 = ts1[np.argmin([distance_to_point(t, path1, origin1) for t in ts1])]
        t2 = ts2[np.argmin([distance_to_point(t, path2, origin2) for t in ts2])]

        base1 = path1(t1)
        base2 = path2(t2)
        default_length = np.max([tensor1.stroke_style.width,
                                 tensor2.stroke_style.width])
        default_length = np.min([default_length, np.linalg.norm(disp12)/4])
        leg_lengths = kwargs.get('leg_lengths', [default_length]*2)
        dir12 = (disp12)/np.linalg.norm(disp12)
        tip1 = Position(*(base1 + dir12 * leg_lengths[0]), inclination)
        tip2 = Position(*(base2 - dir12 * leg_lengths[1]), orientation(-dir12))

        leg_kwargs = kwargs.get('leg_kwargs', [{},{}])
        tensor1.legs.append(Leg(tensor1, tip1, base1, **leg_kwargs[0]))
        tensor2.legs.append(Leg(tensor2, tip2, base2, **leg_kwargs[1]))

        return self._contract_legs(tensor1_idx, -1, tensor2_idx, -1, **kwargs)

    def contract(self, *args, **kwargs):
        if(len(args) == 2):
            return self._contract_tensors(*args, **kwargs)
        elif(len(args) == 4):
            return self._contract_legs(*args, **kwargs)

    def _update_window(self, xmin, xmax, ymin, ymax):
        self.window[0] = np.min([self.window[0], xmin])
        self.window[1] = np.max([self.window[1], xmax])
        self.window[2] = np.min([self.window[2], ymin])
        self.window[3] = np.max([self.window[3], ymax])

    def draw_obj(self, obj, position, context):
        xshift = (position.x - self.window[0])
        yshift = (position.y - self.window[2])

        context.save()

        context.translate(xshift, yshift)
        context.rotate(position.orientation)

        obj.draw(context)

        context.restore()

    #def draw_contraction(self, contraction, context)

    def _draw_boundary(self, context, window_height, window_width):
        context.move_to(0,0)
        context.set_source_rgba(1,0,0)
        context.set_line_width(window_height/100)
        context.line_to(window_width,0)
        context.stroke()
        context.move_to(0,window_height)
        context.set_source_rgba(0,0,1)
        context.line_to(window_width,window_height)
        context.stroke()
        context.move_to(0,0)
        context.set_source_rgba(0,1,0)
        context.line_to(0,window_height)
        context.stroke()
        context.move_to(window_width,0)
        context.set_source_rgba(1,0.7,0)
        context.line_to(window_width,window_height)
        context.stroke()

    def _surface(self, path, fig_width, fig_height, padding):
        ext = os.path.splitext(path)[1].lower()

        if ext == ".svg":
            return cairo.SVGSurface(path, fig_width + 2*padding, 
                                    fig_height + 2*padding)
        
        elif ext == ".pdf":
            return cairo.PDFSurface(path, fig_width + 2*padding, 
                                    fig_height + 2*padding)
        elif ext in [".ps", ".eps"]:
            return cairo.PSSurface(path, fig_width + 2*padding,
                                   fig_height + 2*padding)
        else:
            raise ValueError(f"Unsupported format '{ext}'")

    def export(self, path, fig_width = 400, padding = 4, **kwargs):
        window_width = self.window[1] - self.window[0]
        window_height = self.window[3] - self.window[2]
        window_ratio = window_width/window_height

        fig_height = np.ceil(fig_width/window_ratio)
        padding = np.floor(2*padding)/2
        surface = self._surface(path, fig_width, fig_height, padding)
        context = cairo.Context(surface)

        context.translate(padding, padding)  
        context.scale(fig_width/window_width, fig_height/window_height)

        #Flip the y direction
        context.translate(0, window_height)  
        context.scale(1, -1)  

        #context.push_group()

        if kwargs.get('show_boundary', False):
            self._draw_boundary(context, window_height, window_width)

        for i,obj in enumerate(self.objects):
            self.draw_obj(obj, self.positions[i], context)

        context.save()
        context.translate(-self.window[0], -self.window[2])
        for contraction in self.contractions:
            contraction.draw(context)
        context.restore()

        #context.pop_group_to_source()
        #context.paint()
        surface.finish()
