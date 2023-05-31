import socket
import select
#from config import Config
from App.Transport.config import Config


def ACK(__socket, timeout=5):
    try:
        r, _, _ = select.select([__socket], [], [], timeout)
        if __socket in r:
            ack, address = __socket.recvfrom(1024)
            return True
        else:
            return False

    except socket.timeout as e:
        print(e)
        return False


class Receiver:
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.handshake_port = kwargs['handshake_port']
        self.socket_HANDSHAKING = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.c = Config.get_instance()
        self.socket_TEXT, self.socket_MEDIA = None, None

    def run(self):
        self.socket_HANDSHAKING.bind((self.host, self.handshake_port))
        self.wait()

    def wait(self):
        try:
            r, _, _ = select.select([self.socket_HANDSHAKING], [], [], 60)
            if self.socket_HANDSHAKING in r:
                data_bytes, calling_peer_address = self.socket_HANDSHAKING.recvfrom(1024)
                data_string = data_bytes.decode('utf-8')
                if data_string == 'REQUEST':
                    self.socket_HANDSHAKING.sendto(b'ACK', calling_peer_address)
                    response = input(f'Request Received From {calling_peer_address[0]}, 1-accept, anything-reject')
                    msg = 'ACCEPTED' if response == '1' else 'REJECTED'
                    self.socket_HANDSHAKING.sendto(msg.encode('utf-8'), calling_peer_address)
                    self.start_connection(calling_peer_address[0])
            else:
                print('timeout exceeded')

        except socket.timeout:
            print('timeout exceeded')

    def start_connection(self, expected_ip):
        self.socket_TEXT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_MEDIA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_TEXT.bind((self.c.config['HOST'], self.c.config['TEXT-PORT']))
        self.socket_MEDIA.bind((self.c.config['HOST'], self.c.config['MEDIA-PORT']))
        self.socket_TEXT.listen()
        while True:
            tcp_conn, tcp_address = self.socket_TEXT.accept()
            if tcp_address[0] == expected_ip:
                break
        print(f'tcp connection from {tcp_address}')


class Sender:
    def __init__(self):
        self.socket_HANDSHAKING = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_TEXT, self.socket_MEDIA = None, None
        self.c = Config.get_instance()

    def run(self, **kwargs):
        self.send_request(kwargs['address'])

    def send_request(self, address):
        self.socket_HANDSHAKING.sendto('REQUEST'.encode('utf-8'), address)
        if not ACK(self.socket_HANDSHAKING, timeout=5):
            print("can not connect to peer")
            return
        response, address = self.socket_HANDSHAKING.recvfrom(1024)
        if response.decode('utf-8') == 'ACCEPTED':
            self.start_connection(address[0])
        else:
            print('rejected')
        return

    def start_connection(self, target_peer_ip):
        self.socket_TEXT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_MEDIA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_TEXT.connect((target_peer_ip, self.c.config['TEXT-PORT']))
        print('tcp connection...')
