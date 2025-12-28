import cairo
import numpy as np

from .polygon import Polygon

# TODO: add_hole from a polygon object
# TODO: HoledCircle
# TODO: Check if hole is inside polygon?

class HoledPolygon(Polygon):
    def __init__(self, vertices, **kwargs):
        super().__init__(vertices, **kwargs)
        self.holes = []

    def add_hole(self, vertices, **kwargs):
        self.holes.append(Polygon(vertices, **kwargs))

    def draw(self, context):
        context.set_fill_rule(cairo.FillRule.EVEN_ODD)

        self.cairo_path(context)
        for hole in self.holes:
            hole.cairo_path(context)

        self.stroke_and_fill(context)
        for leg in self.legs:
            leg.draw(context)

        context.set_fill_rule(cairo.FillRule.WINDING)
        
