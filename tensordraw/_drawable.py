from abc import ABC, abstractmethod

from .stroke_style import StrokeStyle
from .fill_style import FillStyle

class Drawable(ABC):
    def __init__(self, **kwargs):
        self.fill_style = FillStyle()
        self.stroke_style = StrokeStyle()

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
        self.fill_style.fill_preserve(context)
        self.stroke_style.stroke(context)
