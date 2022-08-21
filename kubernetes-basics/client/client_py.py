import socket
import time
import threading
import json
import os

file_name = "client.json"
file_open = open('client.json')
data = json.load(file_open)

SERVER = os.getenv('SERVER_ADD')
PORT = data['SERVER_PORT']
ADDR = (SERVER, PORT)
MSG_WAIT = (int(data['TIME_LOWER']) + int(data['TIME_UPPER'])) / 2
print(SERVER)

MSG_LENGTH = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "0"


def connect():
    """
    Tries to connect to server socket
    :return: client object, connected to server
    """
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
    """
    Sends message to server via client object
    :param client: client object
    :param msg: message to be sent
    :return: None
    """
    while True:
        time.sleep(MSG_WAIT)
        message = msg.encode(FORMAT)
        client.send(message)


def server_reply(client):
    """
    Receives messages from server - prints message
    :param client: client socket object
    :return: None
    """
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
            # Create threads to asynchronously send and receive messages
            if threading.active_count() < 2:
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
