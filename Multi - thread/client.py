import socket
from hashlib import md5
import os
import pickle
from consts import *
from threading import Thread


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._cpu_cores = os.cpu_count()
        self._list_ranges_per_thread = []
        self._given_ranges_global = []

    def start(self):
        """
        Connects to server and initiates the main loop.
        """
        self._sock.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print(f"cpu count:{self._cpu_cores}")
        print(f"connected to server. IP:{SERVER_IP_ADDRESS}, PORT:{SERVER_PORT}.")
        self.main_loop()

    @staticmethod
    def try_decode(range_tuple):
        """
        1. Receives the edges of the range it needs to process from the ranges list.
        2. Goes through the given range and converts each number to MD5 and compares to given hash to check answer.
        3. returns the correct number if it finds it, otherwise 0.
        4. The program runs multiple instances of this function in parallel to maximise results.
        """
        for num in range(range_tuple[0], range_tuple[1]):
            # print(num)
            if md5(str(num).encode()).hexdigest().upper() == CODE:
                return num
        return 0

    def allocate_sub_range(self):
        """
        Splits the given range into even smaller ranges and places them into a list of tuples.
        """
        self._list_ranges_per_thread = []
        for num in range(0, self._cpu_cores):
            start = self._given_ranges_global[0]
            finish = start + ((self._cpu_cores**10) // 2)
            self._list_ranges_per_thread.append(tuple([start, finish]))
            self._given_ranges_global[0] = finish
            print(self._list_ranges_per_thread)

    def thread_setup(self):  # TODO: how to get returns from threads????
        for rng in self._list_ranges_per_thread:
            calc_thread = Thread(target=self.try_decode, args=rng)
            calc_thread.start()
            calc_thread.join()
        return 0

    def main_loop(self):
        """
        1. Sends the initial message containing the threads cpu core count.
        2. Calls the try_decode function and returns the result to the server.
        """
        self._sock.sendall(pickle.dumps(tuple([self._cpu_cores])))  # initial message
        self._given_ranges_global = list(pickle.loads(self._sock.recv(BUFFER_SIZE)))
        self.allocate_sub_range()
        result = self.thread_setup()  # TODO: put the results of all the threads into a list take the max num.
        if result != 0:
            self._sock.sendall(pickle.dumps(tuple([result])))
        else:
            self._sock.sendall(pickle.dumps(tuple([0])))


def main():
    client = Client()
    client.start()


if __name__ == '__main__':
    main()
