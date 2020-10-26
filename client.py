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
        """
        Connects to server and initiates the main loop.
        """
        self._sock.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print(f"cpu count:{self._cpu_cores}")
        print(f"connected to server. IP:{SERVER_IP_ADDRESS}, PORT:{SERVER_PORT}.")
        self.main_loop()

    def try_decode(self):
        """
        1. Receives the edges of the range it needs to process from server.
        2. Goes through the given range and converts each number to MD5 and compares to given hash to check answer.
        3. returns the correct number if it finds it, otherwise 0.
        """
        range_edges_tuple = pickle.loads(self._sock.recv(BUFFER_SIZE))
        for num in range(range_edges_tuple[0], range_edges_tuple[1]):
            print(num)
            if md5(str(num).encode()).hexdigest().upper() == CODE:
                return num
        return 0

    def main_loop(self):
        """
        1. Sends the initial message containing the threads cpu core count.
        2. Calls the try_decode function and returns the result to the server.
        """
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
