class TargetGetterProxy:
    def __init__(self, ctx, target):
        self.ctx = ctx
        self.target = target

    def get(self):
        return getattr(self.ctx, self.target)

    def __str__(self):
        return str(self.get())
