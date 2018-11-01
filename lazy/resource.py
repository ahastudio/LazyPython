from .lazy import lazy


class Resource(object):

    def __init__(self, f, g, middle):
        self.f = f
        self.g = g
        self.middle = middle

    def use(self, excuter):
        @lazy
        def dummy():
            self.file = self.f.excute()
            return excuter(self.file)
        self.middle = dummy()
        return Resource(self.f, self.g, self.middle)

    def map(self, f):
        self.middle = self.middle & f
        return Resource(self.f, self.g, self.middle)

    def flatMap(self, f):
        self.middle = self.middle << f
        return Resource(self.f, self.g, self.middle)

    def excute(self):
        result = self.middle.excute()
        self.g(self.file)
        return result

    @staticmethod
    def make(f):
        return Resource._relese(f)

    @staticmethod
    def _relese(f):
        _f = f

        def relese(g):
            return Resource(_f, g, lazy(lambda x: x))
        return relese