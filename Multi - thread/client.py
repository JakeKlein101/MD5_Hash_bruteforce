import socket
from hashlib import md5
import os
import pickle
from consts import *
import threading


class ThreadEnd(Exception):
    def __init__(self):
        Exception.__init__(self)


class Client:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._cpu_cores = os.cpu_count()
        self._list_ranges_per_thread =[]
        self._given_ranges_global = []
        self._result_list = []

    def start(self):
        """
        Connects to server and initiates the main loop.
        """
        self._sock.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print(f"cpu count:{self._cpu_cores}")
        print(f"connected to server. IP:{SERVER_IP_ADDRESS}, PORT:{SERVER_PORT}.")
        self.main_loop()

    def try_decode(self, start, finish):  # TODO: fix threading
        """
        1. Receives the edges of the range it needs to process from the ranges list.
        2. Goes through the given range and converts each number to MD5 and compares to given hash to check answer.
        3. returns the correct number if it finds it, otherwise 0.
        4. The program runs multiple instances of this function in parallel to maximise results.
        """
        print("Thread Started")
        for num in range(start, finish):
            if md5(str(num).encode()).hexdigest().upper() == CODE:
                print(num)
                self._result_list.append(num)
                raise ThreadEnd
        self._result_list.append(0)

    def allocate_sub_range(self):
        """
        Splits the given range into even smaller ranges and places them into a list of tuples.
        """
        self._list_ranges_per_thread = []
        for num in range(0, self._cpu_cores):
            start = self._given_ranges_global[0]
            finish = start + (self._cpu_cores**9)
            if finish > self._given_ranges_global[1]:
                break
            self._list_ranges_per_thread.append(tuple([start, finish]))
            self._given_ranges_global[0] = finish
        print(f"the ranges:{self._list_ranges_per_thread}")

    def thread_setup(self):
        thread_list = [threading.Thread(target=self.try_decode, args=(rng[0], rng[1]), daemon=True) for rng in
                       self._list_ranges_per_thread]
        for th in thread_list:
            th.start()
        for th in thread_list:
            th.join()

    def main_loop(self):
        """
        1. Sends the initial message containing the threads cpu core count.
        2. Calls the try_decode function and returns the result to the server.
        """
        self._sock.sendall(pickle.dumps(tuple([self._cpu_cores])))  # initial message
        self._given_ranges_global = list(pickle.loads(self._sock.recv(BUFFER_SIZE)))
        self.allocate_sub_range()
        self.thread_setup()
        result = max(self._result_list)
        if result != 0:
            self._sock.sendall(pickle.dumps(tuple([result])))
        else:
            self._sock.sendall(pickle.dumps(tuple([0])))


def main():
    client = Client()
    client.start()


if __name__ == '__main__':
    main()
