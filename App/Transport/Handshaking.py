import socket
import select


def wait(__socket, timeout=5):
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
        self.port = kwargs['port']
        self.socket_HANDSHAKING = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_HANDSHAKING.bind((self.host, self.port))

    def run(self):
        self.wait()

    def wait(self):
        # self.socket.settimeout(60)
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
            else:
                print('timeout exceeded')

        except socket.timeout:
            print('timeout exceeded')

    def bind(self):
        self.socket_HANDSHAKING.bind((self.host, self.port))

    def release(self):
        self.socket_HANDSHAKING.close()


class Sender:
    def __init__(self):
        self.socket_HANDSHAKING = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self, **kwargs):
        self.send_request(kwargs['address'])

    def send_request(self, address):
        self.socket_HANDSHAKING.sendto('REQUEST'.encode('utf-8'), address)
        if not wait(self.socket_HANDSHAKING, timeout=10):
            print("can not connect to peer")
            return
        response, address = self.socket_HANDSHAKING.recvfrom(1024)
        if response.decode('utf-8') == 'ACCEPTED':
            print('done')
        else:
            print('rejected')
        return
