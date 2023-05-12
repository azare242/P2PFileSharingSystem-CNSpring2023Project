import socketserver
from http.server import BaseHTTPRequestHandler
import json
from RedisConnection import RedisConnection
import config

class STUNHandler(BaseHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer):
        self.redis_connection = RedisConnection(HOST=config.get('HOST'), PORT=config.get('REDIS-PORT'), db=config.get('REDIS-DB'))
        super().__init__(request, client_address, server)


    def sign_up(self, username, ip):
        """
        TODO: ADD TO CACHE
        :return:
        STATUS
        """
        return {'message': self.redis_connection.set(username, ip)}

    def get_all_peers(self):
        """
        TODO: GET ALL PEERS
        :return: PEER LIST
        """

        return {'all': self.redis_connection.get_all_keys()}

    def get_peer(self, username):
        """
        TODO: GET PEER IP
        :param username: PEER USERNAME
        :return: PEER IP
        """
        return {'ip': self.redis_connection.get_by_key(username)}

    def do_GET(self):
        path = self.path
        print(path)
        if path == '/getall':
            response = self.get_all_peers()
        elif '/getpeerip' in path:
            response = self.get_peer(path.split('?')[1].split('=')[1])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        path = self.path
        print(path)
        length = int(self.headers.get('Content-Length', 0))
        request_body = self.rfile.read(length).decode('utf-8')
        body_dict = json.loads(request_body)
        if path == '/signup':
            response = self.sign_up(body_dict['username'], body_dict['ip'])
        else:
            response = {'message': 'wtf?'}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
