import random
from http.server import BaseHTTPRequestHandler
import json


class STUNHandler(BaseHTTPRequestHandler):

    def sign_up(self, username, ip):
        """
        TODO: ADD TO CACHE
        :return:
        None
        """
        print(username, ip)
        return {'message': 'signed up successfully'}

    def get_all_peers(self):
        """
        TODO: GET ALL PEERS
        :return: PEER DICTIONARY
        """
        import random, string
        alph = string.ascii_lowercase
        num = string.digits
        li = [''.join(random.choice(alph + num) for i in range(10)) for j in range(5)]
        return {'all': li}

    def get_peer(self, username):
        """
        TODO: GET PEER IP
        :param username: PEER USERNAME
        :return: PEER IP
        """
        import random
        print(username)
        ip = '.'.join([str(random.randint(10, 250)) for _ in range(4)])
        return {'ip': ip}

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
