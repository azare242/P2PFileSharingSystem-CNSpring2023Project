import select
import socket
from Transport import *


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


class UISender:
    def __init__(self):
        self.socket_HANDSHAKING = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_TEXT, self.socket_MEDIA = None, None
        self.c = Config.get_instance()

    def run(self, **kwargs):
        self.send_request(kwargs['address'])

    def send_request(self, address):
        self.socket_HANDSHAKING.sendto('REQUEST'.encode('utf-8'), address)
        if not ACK(self.socket_HANDSHAKING, timeout=5):
            # TODO: RETURN STATUS
            pass
        response, address = self.socket_HANDSHAKING.recvfrom(1024)
        if response.decode('utf-8') == 'ACCEPTED':
            # TODO: START COMMUNICATE
            pass
        else:
            # TODO: RETURN REJECT STATUS
            pass
        return

    def send_file(self, abspath, target_peer_ip):
        img = Image.open(abspath)
        data_bytes = img.tobytes()
        wb = str(img.size[0]).encode('utf-8')
        hb = str(img.size[1]).encode('utf-8')
        self.socket_MEDIA.sendto(wb, (target_peer_ip, self.c.config['MEDIA-PORT']))
        self.socket_MEDIA.sendto(hb, (target_peer_ip, self.c.config['MEDIA-PORT']))
        block_size = 1024
        for pointer in range(0, len(data_bytes), block_size):
            while True:
                L = pointer
                R = pointer + block_size
                self.socket_MEDIA.sendto(data_bytes[L:R], (target_peer_ip, self.c.config['MEDIA-PORT']))
                if ACK(self.socket_MEDIA):
                    break
        self.socket_MEDIA.sendto(b'EOF', (target_peer_ip, self.c.config['MEDIA-PORT']))

    def check_file(self, target_peer_ip):
        file_name = self.socket_TEXT.recv(1024)
        ans = ''
        # ans = input(
        #     f'peer wants "{file_name.decode("utf-8")}" you have it? if you have enter "y" and if you dont enter "n": ')
        # TODO: GET RESPONSE
        if ans.lower() == 'n':
            self.socket_TEXT.send(b'NO')
            return
        else:
            abspath = ''
            while True:
                abspath = ''
                # TODO: GET FILE PATH
                if check_path(abspath):
                    break
                else:
                    # TODO : SHOW ERROR
                    pass
            self.socket_TEXT.send(b'YES')
            _ = self.socket_TEXT.recv(1024)
            self.send_file(abspath, target_peer_ip)


class UIReceiver:
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
                        # TODO: START COMMUNICATE
                        pass
            else:
                # TODO: RETURN TIMEOUT STATUS
                pass

        except socket.timeout:
            # TODO: RETURN TIMEOUT STATUS
            pass

    def get_file(self):
        w_data, _ = self.socket_MEDIA.recvfrom(1024)
        h_data, _ = self.socket_MEDIA.recvfrom(1024)
        w = int(w_data.decode('utf-8'))
        h = int(h_data.decode('utf-8'))
        ch = []
        while True:
            chun, add = self.socket_MEDIA.recvfrom(1024)
            if chun == b'EOF':
                break
            ch.append(chun)
            self.socket_MEDIA.sendto(b'ACK', add)
        media_bytes = b''.join(ch)
        save_path = ''
        # TODO: GET SAVE PATH
        Image.frombytes("RGB", (w, h), media_bytes).save(save_path)

    def description_file(self, expected_ip, tcp_conn):
        description = ''
        # TODO: GET DESCRIPTION
        tcp_conn.send(description.encode('utf-8'))
        response = tcp_conn.recv(1024)
        if response.decode('utf-8') == 'YES':
            tcp_conn.send(b'ok')
            self.get_file()
        else:
            # TODO: SHOW MESSAGE
            pass
