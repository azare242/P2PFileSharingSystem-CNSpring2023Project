from STUNServer import STUNServer

if __name__ == '__main__':
    server = STUNServer(HOST='localhost', PORT=8888)
    server.run()