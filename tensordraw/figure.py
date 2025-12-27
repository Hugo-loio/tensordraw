import cairo
import numpy as np

from .utils import Position
from .utils import rotation

class Figure():
    def __init__(self):
        self.objects = []
        self.positions = []
        self.contractions = []
        # Window limits [xmin, xmax, ymin, ymax]
        self.window = []

    def place(self, obj, x, y, orientation = 0):
        self.objects.append(obj)
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
        #print(self.window)

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

    def export(self, path, fig_width = 400, padding = 4, **kwargs):
        window_width = self.window[1] - self.window[0]
        window_height = self.window[3] - self.window[2]
        window_ratio = window_width/window_height

        fig_height = np.ceil(fig_width/window_ratio)
        padding = np.floor(2*padding)/2
        surface = cairo.PDFSurface(path, fig_width + 2*padding, fig_height + 2*padding)
        context = cairo.Context(surface)

        context.translate(padding, padding)  
        context.scale(fig_width/window_width, fig_height/window_height)

        #Flip the y direction
        context.translate(0, window_height)  
        context.scale(1, -1)  

        context.push_group()

        if kwargs.get('show_boundary', False):
            self._draw_boundary(context, window_height, window_width)

        for i,obj in enumerate(self.objects):
            self.draw_obj(obj, self.positions[i], context)

        context.pop_group_to_source()
        context.paint()
