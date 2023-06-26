import socket
import select
from PIL import Image

# from config import Config
from App.Transport.config import Config


def check_path(path):
    try:
        f = open(path, 'rb')
        f.close()
        return True
    except:
        return False


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
                    if response == '1':
                        self.start_connection(calling_peer_address[0])
            else:
                print('timeout exceeded')

        except socket.timeout:
            print('timeout exceeded')

    def get_file_(self):
        try:
            r, _, _ = select.select([self.socket_MEDIA], [], [], 10)
            if self.socket_MEDIA in r:
                data, address = self.socket_MEDIA.recvfrom(1024)
                return data, address
            else:
                return None, None

        except socket.timeout as e:
            return None, None

    def get_file(self):
        w_data, _ = self.get_file_()
        if w_data is None:
            print('connection lost')
            return
        h_data, _ = self.get_file_()
        if h_data is None:
            print('connection lost')
            return
        w = int(w_data.decode('utf-8'))
        h = int(h_data.decode('utf-8'))
        ch = []
        while True:
            chun, add = self.get_file_()
            if chun is None:
                print('connection lost')
                return
            if chun == b'EOF':
                break
            ch.append(chun)
            self.socket_MEDIA.sendto(b'ACK', add)
        media_bytes = b''.join(ch)
        save_path = input('enter abspath for save file:')
        Image.frombytes("RGB", (w, h), media_bytes).save(save_path)

    def description_file(self, expected_ip, tcp_conn):
        description = input('enter your description of what file you want from peer: ')
        try:
            tcp_conn.send(description.encode('utf-8'))
            response = tcp_conn.recv(1024)
            if response.decode('utf-8') == 'YES':
                tcp_conn.send(b'ok')
                self.get_file()
            else:
                print(f'peer does not have {description}')
        except socket.error:
            print('connection lost')
            return

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
        tcp_conn.send(b'hey')
        data, udp_address = self.socket_MEDIA.recvfrom(1024)
        if udp_address[0] == expected_ip and data.decode() == 'MEDIA-CONNECTION':
            self.socket_MEDIA.sendto(b'CONNECTION ACCEPTED', udp_address)
            print(f'udp connection from {udp_address}')
            self.description_file(expected_ip, tcp_conn)


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

    def send_file(self, abspath, target_peer_ip):
        img = Image.open(abspath)
        data_bytes = img.tobytes()
        wb = str(img.size[0]).encode('utf-8')
        hb = str(img.size[1]).encode('utf-8')
        self.socket_MEDIA.sendto(wb, (target_peer_ip, self.c.config['MEDIA-PORT']))
        self.socket_MEDIA.sendto(hb, (target_peer_ip, self.c.config['MEDIA-PORT']))
        block_size = 1024
        resend_counter = 0
        for pointer in range(0, len(data_bytes), block_size):
            while True:
                if resend_counter == 3:
                    print('connection lost')
                    return
                resend_counter += 1
                L = pointer
                R = pointer + block_size
                self.socket_MEDIA.sendto(data_bytes[L:R], (target_peer_ip, self.c.config['MEDIA-PORT']))
                if ACK(self.socket_MEDIA):
                    resend_counter = 0
                    break

        self.socket_MEDIA.sendto(b'EOF', (target_peer_ip, self.c.config['MEDIA-PORT']))

    def check_file(self, target_peer_ip):
        try:
            file_name = self.socket_TEXT.recv(1024)
        except socket.error:
            print('connection lost')
            return

        ans = input(
            f'peer wants "{file_name.decode("utf-8")}" you have it? if you have enter "y" and if you dont enter "n": ')

        if ans.lower() == 'n':
            self.socket_TEXT.send(b'NO')
            return
        else:
            abspath = ''
            while True:
                abspath = input('enter abspath: ')
                if check_path(abspath):
                    break
                else:
                    print('no such valid file', end=' ')
            self.socket_TEXT.send(b'YES')
            _ = self.socket_TEXT.recv(1024)
            self.send_file(abspath, target_peer_ip)

    def start_connection(self, target_peer_ip):
        self.socket_TEXT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_MEDIA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_TEXT.connect((target_peer_ip, self.c.config['TEXT-PORT']))
        print(self.socket_TEXT.recv(1024).decode('utf-8'))
        print('tcp connected...')
        self.socket_MEDIA.sendto(b'MEDIA-CONNECTION', (target_peer_ip, self.c.config['MEDIA-PORT']))
        data, udp_address = self.socket_MEDIA.recvfrom(1024)
        if udp_address[0] == target_peer_ip and data.decode() == 'CONNECTION ACCEPTED':
            print('udp connected...')
            self.check_file(target_peer_ip)
