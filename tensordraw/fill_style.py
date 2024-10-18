class FillStyle():
    def __init__(self, **kwargs):
        # Default values
        self.color = (0,0,1,1)

        self.set(**kwargs)

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def fill_preserve(self, context):
        context.set_source_rgba(*self.color)
        context.fill_preserve()
