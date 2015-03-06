import rsa
import json
import sys
import logging
import logging.handlers
import socket
import struct


server_list = None
logger = None


class ClientSocket:

    pubkey = None

    def __init__(self):
        #load pub key
        path = sys.path[0]
        if not self.pubkey:
            with open(path + "/public.pem") as pubfile:
                p = pubfile.read()
                self.pubkey = rsa.PublicKey.load_pkcs1(p)

        #init socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(20)

    def connect(self, server, port):
        self.sock.connect((server, port))

    def __crypto(self, command):
        return rsa.encrypt(command, self.pubkey)

    def send_command(self, command):
        data = self.__crypto(command)
        send_len = struct.pack('i', len(data))
        self.sock.send(send_len)
        self.sock.send(data)


    def receive_result(self):
        length = self.sock.recv(4)
        if length == "":
            raise RuntimeError("socket connection broken")
        length, = struct.unpack('i', length)
        logger.debug("receive data length is {0}".format(length))
        bytes_read = 0
        answer = []
        while bytes_read < length:
            data = self.sock.recv(min(length - bytes_read, 2048))
            if data == "":
                raise RuntimeError("socket connection broken")
            answer.append(data)
            bytes_read += len(data)
        logger.debug("".join(answer))

    def close(self):
        self.sock.close()


def init_log():
    path = sys.path[0]
    handler = logging.handlers.RotatingFileHandler(path + "/update.log", maxBytes=1024 * 1024, backupCount=5)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    global logger
    logger = logging.getLogger('update')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def read_server_list():
    path = sys.path[0]
    fp = file(path + "/server_list.json")
    obj = json.load(fp)
    global server_list
    server_list = obj["server"]


def send_update(server):
    global logger
    logger.debug("begin update server {0}".format(server))
    sock = ClientSocket()
    try:
        sock.connect(server["ip"], server["port"])
        sock.send_command("update")
        sock.receive_result()
    except Exception, e:
        logger.error("connect to server {0}:{1} error!".format(server["ip"], server["port"]))
    finally:
        sock.close()
        logger.debug("update server finished {0}".format(server))


def update():
    global server_list
    for server in server_list:
        send_update(server)


def main():
    init_log()
    read_server_list()
    update()


if __name__ == '__main__':
    main()