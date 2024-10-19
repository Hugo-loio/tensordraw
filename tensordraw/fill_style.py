class FillStyle():
    def __init__(self, **kwargs):
        # Default values
        self.color = (0,0,1,1)

        self.set(**kwargs)

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def _prepare_context(self, context):
        context.set_source_rgba(*self.color)

    def fill_preserve(self, context):
        self._prepare_context(context)
        context.fill_preserve()

    def fill(self, context):
        self._prepare_context(context)
        context.fill()
