from .color import Color

class FillStyle():
    def __init__(self, **kwargs):
        # Default values
        self._color = Color()
        self.default = {key : True for key in self.__dict__.keys()}

        self.set(**kwargs)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color.set(val)

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                self.default[key] = False

    def _prepare_context(self, context):
        context.set_source_rgba(*self._color.color)

    def fill_preserve(self, context):
        self._prepare_context(context)
        context.fill_preserve()

    def fill(self, context):
        self._prepare_context(context)
        context.fill()
