import json
from HTTPConnection import HTTPConnection


class Peer:
    def __init__(self, **kwargs):
        f = open('url.json', 'r')
        self.urls = json.load(f)
        f.close()
        self.http = HTTPConnection()
        self.response = None

    def get_all_peers(self):
        self.response = json.loads(self.http.get(self.urls['GETALL']).text)
        for x in self.response['all']:
            print(x)

    def signup(self, username, ip):
        self.response = json.loads(self.http.post(self.urls['SIGNUP'], json={'username': username, 'ip': ip}).text)
        print(self.response['message'])

    def get_peer_ip(self, username):
        self.response = json.loads(self.http.get(self.urls['GETPEERIP'], params={'username': username}).text)
        for un, _ip in self.response.items():
            x = f'{un}: {_ip}' if _ip != 'NOT EXISTS' else _ip
            print(x)

    def run(self):
        while True:
            command = input('>> ').lower()
            if command == 'help':
                print('get-all-peers -> get all peers in system by username\nget-peer-ip <username> -> get peer ip by '
                      'username\nsignup <username> <ip> -> add your ip and username in system')

            elif command == 'get-all-peers':
                self.get_all_peers()

            elif 'signup' in command:
                args = command.split()
                if len(args) == 3:
                    username, ip = args[1:]
                    self.signup(username, ip)
                else:
                    print('signup <username> <ip>')

            elif 'get-peer-ip' in command:
                args = command.split()
                if len(args) == 2:
                    username = args[1]
                    self.get_peer_ip(username)
                else:
                    print('get-peer-ip <username>')
            elif command == 'exit':
                return
            else:
                print('invalid')


