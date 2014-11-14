class Manager(object):
    def __init__(self):
        self._resources = {}

    def __getattribute__(self, name):
        return self._resources.get(name)
