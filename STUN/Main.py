from STUNServer import STUNServer
import config

if __name__ == '__main__':
    #print(config.get('PORT'))
    server = STUNServer(HOST=config.get('HOST'), PORT=config.get('STUN-PORT'))
    server.run()
