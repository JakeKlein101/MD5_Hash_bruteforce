import socket
from hashlib import md5
import os
import pickle
from consts import *


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._cpu_cores = os.cpu_count()

    def start(self):
        self._sock.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print(f"cpu count:{self._cpu_cores}")
        print(f"connected to server. IP:{SERVER_IP_ADDRESS}, PORT:{SERVER_PORT}.")
        self.main_loop()

    def try_decode(self):
        equal = False
        num = 0
        range_generator = (x for x in range(10**9, 10**10))
        while not equal and num < 10**10:
            num = next(range_generator)
            print(num)
            if md5(str(num).encode()).hexdigest().upper() == CODE:
                equal = True
        if not equal:
            return 0
        return num

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
