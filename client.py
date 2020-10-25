import socket
from hashlib import md5
import os
import pickle
from consts import *


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._cpu_count = os.cpu_count()

    def start(self):
        self._sock.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print(f"cpu count:{self._cpu_count}")
        print(f"connected to server. IP:{SERVER_IP_ADDRESS}, PORT:{SERVER_PORT}.")
        self.main_loop()

    def try_decode(self):
        ranges = pickle.loads(self._sock.recv(BUFFER_SIZE))
        for num in ranges:
            if md5(num.encode()).hexdigest().upper() == CODE:
                return True
        return False

    def main_loop(self):
        while True:
            if self.try_decode():
                self._sock.sendall(pickle.dumps(tuple([0])))
                break


def main():
    client = Client()
    client.start()


if __name__ == '__main__':
    main()
