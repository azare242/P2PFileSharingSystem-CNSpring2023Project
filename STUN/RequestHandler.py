import socketserver
from http.server import BaseHTTPRequestHandler
import json
from RedisConnection import RedisConnection
import config


class STUNHandler(BaseHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer):
        self.redis_connection = RedisConnection(HOST=config.get('HOST'), PORT=config.get('REDIS-PORT'),
                                                db=config.get('REDIS-DB'))
        super().__init__(request, client_address, server)

    def sign_up(self, username, ip):
        """
        :return:
        STATUS
        """
        return {'message': self.redis_connection.set(username, ip)}

    def get_all_peers(self):
        """
        :return: PEER LIST
        """

        return {'all': self.redis_connection.get_all_keys()}

    def get_peer(self, username):
        """
        :param username: PEER USERNAME
        :return: PEER IP
        """
        return {'ip': self.redis_connection.get_by_key(username)}

    def read_json_from_body(self):
        """

        :return: json dict from http request body
        """
        length = int(self.headers.get('Content-Length', 0))
        request_body = self.rfile.read(length).decode('utf-8')
        return json.loads(request_body)

    def do_GET(self):
        path = self.path
        print(path)
        if path == '/getall':
            response = self.get_all_peers()
            status = 200
        elif '/getpeerip' in path:
            response = self.get_peer(self.read_json_from_body()['username'])
            status = 404 if response['ip'] == 'NOT EXISTS' else 200
        else:
            response = {'message': 'bad request'}
            status = 400
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        path = self.path
        body_dict = self.read_json_from_body()
        if path == '/signup':
            response = self.sign_up(body_dict['username'], body_dict['ip'])
            status = 200 if response['message'] == 'SUCCESSFUL' else 406
        else:
            response = {'message': 'bad request'}
            status = 400

        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
