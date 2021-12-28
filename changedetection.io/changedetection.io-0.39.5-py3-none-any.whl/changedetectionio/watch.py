class url_watch(dict):
    def __init__(self, *args):
        super().__init__(args)

    def dates(self, function):
        return [function(i) for i in self]