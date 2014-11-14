class TestRestController(SimpleRest):
    CONTENT_TYPE = 'json'

    def __init__(self):
        pass

    def get_object(self, pk):
        return pk

    def create(self, **data):
        pass

    def update(self, pk, **data):
        pass

    def get(self, pk):
        return serializer(pk)

    def delete(self, pk):
        pass
