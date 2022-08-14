import socket
import threading
import time
from configparser import ConfigParser

file_name = "server.ini"
config = ConfigParser()
config.read(file_name)

"""
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
MSG_WAIT = (1 + 1) // 2
"""
SERVER = '0.0.0.0'
PORT = config['server_config']['SERVER_PORT']
ADDR = (SERVER, PORT)
MSG_WAIT = (int(config['server_config']['TIME_LOWER']) + int(config['server_config']['TIME_UPPER'])) / 2


MSG_LENGTH = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "0"
RETURN_MSG = "I got it, roger"

connection_status = False
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(connection, client_addr):
    print(f"[NEW CONNECTION] {client_addr} connected...")
    global connection_status
    connection_status = True
    connected = True
    while connected:
        message = connection.recv(MSG_LENGTH).decode(FORMAT)
        if message:
            print(f"[{client_addr}] {message}")
        else:
            print(f"[DISCONNECT] {client_addr} disconnecting...")
            connection_status = False
            connected = False
    connection.close()


def send_return(connection):
    return_msg = RETURN_MSG.encode(FORMAT)
    while True:
        time.sleep(MSG_WAIT)
        if connection_status:
            connection.send(return_msg)


def server_main():
    server.listen()
    global connection_status
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, client_addr = server.accept()
        try:
            # handle_client(connection, client_addr)
            if threading.activeCount() < 2:
                thread_handle_client = threading.Thread(target=handle_client, args=(connection, client_addr), daemon=True)
                thread_send_return = threading.Thread(target=send_return, args=(connection,), daemon=True)
                thread_handle_client.start()
                thread_send_return.start()
        except ConnectionResetError or OSError:
            print(f"[CONNECTION REFUSED] disconnected to client")
            connection_status = False
            thread_handle_client.join()
            thread_send_return.join()
            connection.close()
            continue


print("[STARTING] server is starting...")
server_main()
