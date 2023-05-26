import json
from HTTPConnection import HTTPConnection
from Transport import Handshaking, MediaDataTransfer, TextDataTransfer, config


class Peer:
    def __init__(self, **kwargs):
        self.transport_config = config.Config.get_instance()
        f = open('help-message.txt', 'r')
        temp = "".join(f.readlines())
        f.close()
        self.help_message = temp
        f = open('url.json', 'r')
        self.urls = json.load(f)
        f.close()
        self.http = HTTPConnection()
        self.wait, self.sendreq = None, None
        self.response = None
        self.second_peer_ip = None

    def new_wait(self):
        self.wait = Handshaking.Wait(host=self.transport_config.config['HOST'],
                                     port=self.transport_config.config['HANDSHAKE-PORT'])

    def new_sendreq(self):
        self.sendreq = Handshaking.Request(host=self.second_peer_ip,
                                           port=self.transport_config.config['HANDSHAKE-PORT'])

    def end_handshaking(self):
        self.wait, self.sendreq = None, None

    def set_second_peer_ip(self, ip):
        self.second_peer_ip = ip

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

    def wait_for_request(self):
        pass

    def run(self):
        while True:
            command = input('>> ').lower()
            if command == 'help':
                print(self.help_message)

            elif command == 'get-all-peers':
                self.get_all_peers()

            elif 'signup' in command:
                args = command.split()
                if len(args) == 2:
                    username = args[1]
                    ip = self.transport_config.config['HOST']
                    self.signup(username, ip)
                else:
                    print('signup <username>')

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
