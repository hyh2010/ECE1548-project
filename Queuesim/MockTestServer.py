from ServerBase import ServerBase

class MockTestServer(ServerBase):
    def __init__(self, env, resource):
        super().__init__(env, resource)

    def service_time(self):
        return 5
