import socket
from threading import Thread
from hashlib import md5
import os

CODE = "EC9C0F7EDCC18A98B1F31853B1813301"
SERVER_IP_ADDRESS = "127.0.0.1"
SERVER_PORT = 8820


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._cpu_count = os.cpu_count()

    def start(self):
        self._sock.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print(f"cpu count:{self._cpu_count}")
        print(f"connected to server. IP:{SERVER_IP_ADDRESS}, PORT:{SERVER_PORT}.")

    @staticmethod
    def try_decode():
        return md5(CODE.encode()).hexdigest().upper()

    def main_loop(self):
        while True:
            digested = self.try_decode()
            if len(digested) == 10:
                self._sock.sendall(digested.encode())


def main():
    hashed = md5(b"5").hexdigest().upper()
    client = Client()
    client.start()


if __name__ == '__main__':
    main()
