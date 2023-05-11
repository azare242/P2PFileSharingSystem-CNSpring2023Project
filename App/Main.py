from HTTPConnection import HTTPConnection


if __name__ == '__main__':
    con = HTTPConnection()
    while True:
        command = input('>> ')
        if command == 'help':
            print('get-all-peers -> get all peers in system by username\nget-peer-ip <username> -> get peer ip by '
                  'username\nsignup <username> <ip> -> add your ip and username in system')
        elif command == 'get-all-peers':
            print(con.get('http://localhost:8888/getall').text)
        elif 'get-peer-ip' in command:
            username = command.split()[1]
            print(con.get('http://localhost:8888/getpeerip', params={'username': username}).text)
        elif 'signup' in command:
            username, ip = command.split()[1:]
            print(con.post('http://localhost:8888/signup', json={'username': username, 'ip': ip}).text)
        elif command == 'exit':
            break
        else:
            print('wtf? use help command bro')