import json
from HTTPConnection import HTTPConnection
from Transport import Handshaking, config


class Peer:
    def __init__(self, **kwargs):
        self.un = None
        self.urls = {}
        self.http = HTTPConnection()
        self.transport_config = config.Config.get_instance()
        f = open('help-message.txt', 'r')
        temp = "".join(f.readlines())
        f.close()
        self.help_message = temp
        self.construct_urls()
        self.rec, self.snd = None, None
        self.response = None
        self.target_peer_ip = None
        self.all_peers = None
        self.init_program()

    def init_program(self):
        self.un = input('enter username: ')
        print('initializing program...')
        self.signup(self.un, self.transport_config.config['HOST'])
        self.all_peers = self.get_all_peers()
        print(f'signup as {self.un}')

    def construct_urls(self):
        f = open('url.json', 'r')
        temp = json.load(f)
        f.close()
        base_url = f'http://{temp["HTTP-HOST"]}:{temp["HTTP-PORT"]}'
        self.urls['SIGNUP'] = base_url + temp['SIGNUP']
        self.urls['GETPEERIP'] = base_url + temp['GETPEERIP']
        self.urls['GETALL'] = base_url + temp['GETALL']

    def new_rec(self):
        self.rec = Handshaking.Receiver(host=self.transport_config.config['HOST'],
                                        handshake_port=self.transport_config.config['HANDSHAKE-PORT'])

    def new_snd(self):
        self.snd = Handshaking.Sender()

    def end_handshaking(self):
        self.target_peer_ip, self.rec, self.snd = None, None, None

    def set_target_peer_ip(self, ip):
        self.target_peer_ip = ip

    def get_all_peers(self):
        self.response = json.loads(self.http.get(self.urls['GETALL']).text)
        return self.response['all']

    def signup(self, username, ip, SHOW_MESSAGE=False):
        self.response = json.loads(self.http.post(self.urls['SIGNUP'], json={'username': username, 'ip': ip}).text)
        if SHOW_MESSAGE:
            print(self.response['message'])

    def get_peer_ip(self, username, RETURN_IP=False):
        self.response = json.loads(self.http.get(self.urls['GETPEERIP'], json={'username': username}).text)
        result = ''
        for un, _ip in self.response.items():
            x = f'{un}: {_ip}' if _ip != 'NOT EXISTS' else _ip
            if not RETURN_IP:
                print(x)
            else:
                result = _ip
        if RETURN_IP:
            return result

    def wait_for_request(self):
        self.new_rec()
        self.rec.run()
        self.end_handshaking()

    def send_request(self, ip):
        self.set_target_peer_ip(ip)
        self.new_snd()
        self.snd.run(address=(ip, self.transport_config.config['HANDSHAKE-PORT']))
        self.end_handshaking()

    def run(self):

        while True:
            command = input('>> ').lower()
            if command == 'help':
                print(self.help_message)

            elif command == 'get-all-peers':
                for x in self.all_peers:
                    print(f'--{x}')

            elif 'signup' in command:
                args = command.split()
                if len(args) == 2:
                    username = args[1]
                    self.un = username
                    ip = self.transport_config.config['HOST']
                    self.signup(username, ip, SHOW_MESSAGE=True)
                else:
                    print('signup <username>')

            elif command == 'wait-for-requests':
                self.wait_for_request()
            elif 'send-request' in command:
                args = command.split()
                if len(args) == 2:
                    username = args[1]
                    if username not in self.all_peers:
                        print('username not found')
                    else:
                        self.send_request(self.get_peer_ip(username, RETURN_IP=True))
                else:
                    print('send-request <username>')
            elif command == 'exit':
                return
            else:
                print('invalid')
