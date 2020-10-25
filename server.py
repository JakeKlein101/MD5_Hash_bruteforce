import socket
from threading import Thread
import pickle
from consts import *


class Client(Thread):
    def __init__(self, client_socket):
        Thread.__init__(self)
        self._client_socket = client_socket
        self._cpu_cores = 0

    def run(self):
        self.main_loop()

    def main_loop(self):
        self.receive_initial_data()
        ranges = [num for num in range(10**9, 10**10)]
        self._client_socket.sendall(ranges[:self._cpu_cores])
        packet = pickle.loads(self._client_socket.recv(BUFFER_SIZE))
        # if the tuple has only a 0 its a failed attempt, if it has a number its the answer.
        if packet[0] != 0:
            print(f"The result is:{packet[0]}")
        else:
            print("No matches in thread")

    def receive_initial_data(self):
        received_initial_packet = pickle.loads(self._client_socket.recv(BUFFER_SIZE))
        # Initial packet contains only core amount
        self._cpu_cores = received_initial_packet[0]


class Server:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_list = []

    def start(self):
        self._sock.bind((SERVER_IP_ADDRESS, SERVER_PORT))
        self._sock.listen(1)
        print(f"Server has been binded to the IP: {SERVER_IP_ADDRESS} port: {SERVER_PORT}")
        self.server_main_loop()

    def server_main_loop(self):
        while True:
            client_socket, client_address = self._sock.accept()
            print(f"{client_address} just connected")
            client = Client(client_socket)
            self._client_list.append(client)
            client.start()


def main():
    server = Server()
    server.start()


if __name__ == '__main__':
    main()

