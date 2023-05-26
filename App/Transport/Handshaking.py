import socket
import select


class Wait:
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def wait(self):
        self.socket.settimeout(60)
        try:
            r, _, _ = select.select([self.socket], [], [], 60)
            if self.socket in r:
                data_bytes, calling_peer_address = self.socket.recvfrom(1024)
                data_string = data_bytes.decode('utf-8')
                if data_string == 'REQUEST':
                    response = input('Request Received From --somewhere--, 1-accept, anything-reject')
                    msg = 'ACCEPTED' if response == '1' else 'REJECTED'
                    self.socket.sendto(msg.encode('utf-8'), calling_peer_address)
                    # connected to calling peer
                    # implement
            else:
                print('timeout exceeded')

        except socket.timeout:
            print('timeout exceeded')

    def bind(self):
        self.socket.bind((self.host, self.port))

    def release(self):
        self.socket.close()


class Request:
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

    def send_request(self, address):
        self.socket.sendto('REQUEST'.encode('utf-8'), address)
        response = self.socket.recvfrom(1024)
        if response == 'ACCEPTED':
            # connected to receiving peer
            pass
        return
