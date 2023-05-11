from http.server import HTTPServer
from RequestHandler import STUNHandler


class STUNServer:
    def __init__(self, **kwargs):
        # self.redis_connection = Redis_Connection()
        self.server = HTTPServer((kwargs['HOST'], kwargs['PORT']), STUNHandler)

    def run(self):
        self.server.serve_forever()
        self.server.server_close()