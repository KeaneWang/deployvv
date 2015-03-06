import SocketServer
import os
import sys
import json
import subprocess
import rsa
import struct


config_obj = None


class CommandExecer:

    priv_key = None

    def __init__(self, length, data):
        self.length = length
        self.data = data
        if not self.priv_key:
            self.__load_key()

    def __load_key(self):
        path = sys.path[0]
        with open(path + "/../key/private.pem") as privfile:
            p = privfile.read()
            self.priv_key = rsa.PrivateKey.load_pkcs1(p)

    def decrypto(self):
        return rsa.decrypt(self.data, self.priv_key)

    def do_command(self):
        command = self.decrypto()
        print(command)
        if hasattr(self, command):
            return getattr(self, command)()
        else:
            return "error!"

    def update(self):
        path = sys.path[0]
        # exec update.sh and answer the result
        handle = subprocess.Popen(path + "/update.sh", stdout=subprocess.PIPE, shell=False).stdout.readlines()
        print(handle)
        return "".join(handle)


class UpdateHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        length = self.request.recv(4)
        length, = struct.unpack('i', length)
        bytes_read = 0
        tmp_data = []
        while bytes_read < length:
            data = self.request.recv(min(length - bytes_read, 2048))
            if data == "":
                raise RuntimeError("socket error!")
            tmp_data.append(data)
            bytes_read += len(data)

        execer = CommandExecer(length, "".join(tmp_data))
        result = execer.do_command()
        self.request.sendall(struct.pack('i', len(result)))
        self.request.sendall(result)


def load_config_files():
    path = sys.path[0]
    conf_path = path + "/../conf/deploy.json"
    global config_obj
    fp = file(conf_path)
    try:
        config_obj = json.load(fp)
    except Exception, e:
        return False

    return True


def main():
    result = load_config_files()
    if not result:
        print("load config file error!")
        return
    else:
        host = "localhost"
        print("load config file success, listen on port {0}".format(config_obj["port"]))
        server = SocketServer.TCPServer((host, int(config_obj["port"])), UpdateHandler)
        server.serve_forever()


if __name__ == "__main__":
    main()
