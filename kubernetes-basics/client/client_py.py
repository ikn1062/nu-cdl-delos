import socket
import time
import threading
from configparser import ConfigParser
import os

file_name = "client.ini"
config = ConfigParser()
config.read(file_name)

"""
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5051
ADDR = (SERVER, PORT)
MSG_WAIT = (5 + 5)//2
"""
SERVER = os.getenv('SERVER_ADDRESS')
PORT = config['client_config']['SERVER_PORT']
ADDR = (SERVER, PORT)
MSG_WAIT = (int(config['client_config']['TIME_LOWER']) + int(config['client_config']['TIME_UPPER'])) / 2


MSG_LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "0"


def connect():
    timer = 0
    not_connected = True
    client = None
    while not_connected:
        if timer > 0:
            time.sleep(5)
        timer += 1

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(ADDR)
            not_connected = False
        except ConnectionRefusedError as e:
            print(f"[CONNECTION REFUSED] cannot connect to server at {SERVER}")
            continue
    return client


def send(client, msg):
    while True:
        time.sleep(MSG_WAIT)
        message = msg.encode(FORMAT)
        client.send(message)


def server_reply(client):
    while True:
        server_msg = ""
        amount_received = 0
        while not amount_received:
            server_msg = client.recv(64)
            amount_received += len(server_msg)
        print(f"[SERVER] {server_msg.decode(FORMAT)}")


def main():
    while True:
        client = connect()
        client_msg = "Hello World!"
        try:
            # send(client, client_msg)
            if threading.activeCount() < 2:
                thread_send = threading.Thread(target=send, args=(client, client_msg), daemon=True)
                thread_server_reply = threading.Thread(target=server_reply, args=(client,), daemon=True)
                thread_send.start()
                thread_server_reply.start()
        except ConnectionResetError as e:
            print("[CONNECTION REFUSED] disconnected to server")
            thread_send.join()
            thread_server_reply.join()
            client.close()


main()
