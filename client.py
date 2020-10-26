import socket
from hashlib import md5
import os
import pickle
from consts import *


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._cpu_cores = os.cpu_count()
        self._ranges = []

    def start(self):
        self._sock.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print(f"cpu count:{self._cpu_cores}")
        print(f"connected to server. IP:{SERVER_IP_ADDRESS}, PORT:{SERVER_PORT}.")
        self.main_loop()

    def try_decode(self):
        range_edges_tuple = pickle.loads(self._sock.recv(BUFFER_SIZE))
        self._ranges = [num for num in range(range_edges_tuple[0], range_edges_tuple[1])]
        for num in self._ranges:
            if md5(str(num).encode()).hexdigest().upper() == CODE:
                return num
        return 0

    def main_loop(self):
        self._sock.sendall(pickle.dumps(tuple([self._cpu_cores])))  # initial message
        result = self.try_decode()
        if result != 0:
            self._sock.sendall(pickle.dumps(tuple([result])))
        else:
            self._sock.sendall(pickle.dumps(tuple([0])))


def main():
    client = Client()
    client.start()


if __name__ == '__main__':
    main()
