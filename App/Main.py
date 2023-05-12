from HTTPConnection import HTTPConnection
import url

if __name__ == '__main__':
    con = HTTPConnection()
    while True:
        command = input('>> ')
        if command == 'help':
            print('get-all-peers -> get all peers in system by username\nget-peer-ip <username> -> get peer ip by '
                  'username\nsignup <username> <ip> -> add your ip and username in system')
        elif command == 'get-all-peers':
            print(con.get(url.get('GETALL')).text)
        elif 'get-peer-ip' in command:
            username = command.split()[1]
            print(con.get(url.get('GETPEERIP'), params={'username': username}).text)
        elif 'signup' in command:
            username, ip = command.split()[1:]
            print(con.post(url.get('SIGNUP'), json={'username': username, 'ip': ip}).text)
        elif command == 'exit':
            break
        else:
            print('wtf? use help command bro')