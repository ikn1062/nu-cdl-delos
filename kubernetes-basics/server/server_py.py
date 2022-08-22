import socket
import threading
import time
import json

file_name = "server.json"
file_open = open('server.json')
data = json.load(file_open)

SERVER = '0.0.0.0'
PORT = data['SERVER_PORT']
ADDR = (SERVER, PORT)
MSG_WAIT = (int(data['TIME_LOWER']) + int(data['TIME_UPPER'])) / 2
print(ADDR)

MSG_LENGTH = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "0"
RETURN_MSG = "I got it, roger"

connection_status = False
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(connection, client_addr):
    """
    Looking for and setting up connection with client
    - Receives messages when connected to client and prints them out
    :param connection: Client connection
    :param client_addr: Client address
    :return: None
    """
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
    """
    Sends return message to the client
    :param connection: Client connection object
    :return: None
    """
    return_msg = RETURN_MSG.encode(FORMAT)
    while True:
        time.sleep(MSG_WAIT)
        if connection_status:
            connection.send(return_msg)


def server_main():
    # Listens on the service
    server.listen()
    global connection_status
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # Once a client is found, sets up a connection
        connection, client_addr = server.accept()
        try:
            # Create threads to asynchronously send and receive messages
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


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    server_main()
