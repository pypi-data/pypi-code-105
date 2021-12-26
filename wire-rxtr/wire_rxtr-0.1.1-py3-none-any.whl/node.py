class RadixNode(object):
    def __init__(self, path=None, handler=None, methods=None):
        self.path = path
        self.methods = {}
        self.children = []
        self.indices = str()
        self.size = 0

        self.addMethods(methods, handler)

    def __repr__(self):
        return ('<RadixTreeNode path: {}, methods: {}, indices: {}, children: '
                '{}>'.format(self.path, self.methods, self.indices,
                             self.children))

    def addMethods(self, methods, handler):
        if not methods:
            return

        if not isinstance(methods, (list, tuple, set)):
            methods = [methods]

        for method in methods:
            if method in self.methods and self.methods[method] != handler:
                raise KeyError(
                    '{} conflicts with existed handler '
                    '{}'.format(handler, self.methods[method]))

            self.methods[method] = handler

    def bisect(self, target):
        low, high = 0, self.size
        while low < high:
            mid = low + high >> 1
            if self.indices[mid] < target:
                low = mid + 1
            else:
                high = mid
        return low

    def insertChild(self, index, child):
        pos = self.bisect(index)
        self.indices = self.indices[:pos] + index + self.indices[pos:]
        self.children.insert(pos, child)
        self.size += 1

        return child

    def getChild(self, index):
        for i, char in enumerate(self.indices):
            if char == index:
                return self.children[i]