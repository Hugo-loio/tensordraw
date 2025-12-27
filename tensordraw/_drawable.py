from abc import ABC, abstractmethod

import cairo

from .stroke_style import StrokeStyle
from .fill_style import FillStyle

class Drawable(ABC):
    def __init__(self, **kwargs):
        self.fill_style = FillStyle()
        self.stroke_style = StrokeStyle()
        self.operator = "over" # Use of operator not recommended, might break vectorized objects

        self.set(**kwargs)

    def set(self, **kwargs):
        if 'ss' in kwargs:
            kwargs['stroke_style'] = kwargs['ss']
        if 'fs' in kwargs:
            kwargs['fill_style'] = kwargs['fs']
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @abstractmethod
    def draw(self, context):
        pass

    def stroke_and_fill(self, context):
        cairo_operator = f"OPERATOR_{self.operator.upper()}"
        context.set_operator(getattr(cairo, cairo_operator))
        self.fill_style.fill_preserve(context)
        context.set_operator(cairo.OPERATOR_OVER)
        self.stroke_style.stroke(context)
