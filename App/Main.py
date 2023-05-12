from HTTPConnection import HTTPConnection
import url
import json


def json_parser(json_string):
    return json.loads(json_string)


def get_all_peers(response):
    r = json_parser(response)
    for x in r['all']:
        print(x)


def get_peer_ip(response):
    r = json_parser(response)
    for un, _ip in r.items():
        x = f'{un} : {_ip}' if _ip != 'NOT EXISTS' else _ip
        print(x)

def signup(response):
    r = json_parser(response)
    print(r['message'])


if __name__ == '__main__':
    con = HTTPConnection()
    while True:
        command = input('>> ')
        if command == 'help':
            print('get-all-peers -> get all peers in system by username\nget-peer-ip <username> -> get peer ip by '
                  'username\nsignup <username> <ip> -> add your ip and username in system')
        elif command == 'get-all-peers':
            get_all_peers(con.get(url.get('GETALL')).text)
        elif 'get-peer-ip' in command:
            username = command.split()[1]
            get_peer_ip(con.get(url.get('GETPEERIP'), params={'username': username}).text)
        elif 'signup' in command:
            username, ip = command.split()[1:]
            signup(con.post(url.get('SIGNUP'), json={'username': username, 'ip': ip}).text)
        elif command == 'exit':
            break
        else:
            print('wtf? use help command bro')
