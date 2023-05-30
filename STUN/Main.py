from STUNServer import STUNServer
from config import Config

if __name__ == '__main__':
    c = Config.get_instance()
    server = STUNServer(HOST=c.config['HOST'], PORT=c.config['STUN-PORT'])
    server.run()
