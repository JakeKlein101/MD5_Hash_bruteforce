import socket
from threading import Thread
from hashlib import md5
import pickle

CODE = "EC9C0F7EDCC18A98B1F31853B1813301"
IP_ADDRESS = "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Client(Thread):
    def __init__(self, client_socket):
        Thread.__init__(self)
        self._client_socket = client_socket
        self._cpu_count = 0

    def run(self):
        self.receive_data()

    def receive_data(self):
        received_content = pickle.loads(self._client_socket.recv(BUFFER_SIZE))


class Server:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_list = []

    def start(self):
        self._sock.bind((IP_ADDRESS, PORT))
        self._sock.listen(1)
        print(f"Server has been binded to the IP: {IP_ADDRESS} port: {PORT}")
        self.server_main_loop()

    def server_main_loop(self):
        while True:
            client_socket, client_address = self._sock.accept()
            print(f"{client_address} just connected")
            client = Client(client_socket)
            self._client_list.append(client)
            Client.start()


def main():
    server = Server()
    server.start()


if __name__ == '__main__':
    main()

