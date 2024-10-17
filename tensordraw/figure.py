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
            self.window = [xmin, xmax, ymin, ymax]
        else:
            self._update_window(xmin, xmax, ymin, ymax)

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

    def export(self, path, fig_width = 400, padding = 4):
        window_width = self.window[1] - self.window[0]
        window_height = self.window[3] - self.window[2]
        window_ratio = window_width/window_height

        fig_height = fig_width/window_ratio
        surface = cairo.PDFSurface(path, fig_width + 2*padding, fig_height + 2*padding)
        context = cairo.Context(surface)

        context.translate(padding, padding)  
        context.scale(fig_width/window_width, fig_height/window_height)

        #Flip the y direction
        context.translate(0, window_height)  
        context.scale(1, -1)  

        #Auxilary_lines
        context.move_to(0,0)
        context.set_source_rgba(1,0,0)
        context.set_line_width(window_height/100)
        context.line_to(window_width, 0)
        context.stroke()
        context.move_to(0,window_height)
        context.set_source_rgba(0,0,1)
        context.set_line_width(window_height/100)
        context.line_to(window_width, window_height)
        context.stroke()

        for i,obj in enumerate(self.objects):
            self.draw_obj(obj, self.positions[i], context)
