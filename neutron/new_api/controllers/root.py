import pecan

import v2

class RootController(object):
    v2_0 = v2.V2Controller()

    @pecan.expose()
    def _lookup(self, version, *remainder):
        if version == 'v2.0':
            return self.v2_0, remainder
        else:
            pecan.abort(404)

    @pecan.expose('json')
    def index(self):
        return dict()
