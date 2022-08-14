import socket
import threading
import time

PORT = 5050
# SERVER = "0.0.0.0"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
MSG_WAIT = (1 + 1)//2

MSG_LENGTH = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "0"
RETURN_MSG = "I got it, roger"

message_stack = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(connection, client_addr):
    print(f"[NEW CONNECTION] {client_addr} connected...")
    global message_stack
    connected = True
    while connected:
        message = connection.recv(MSG_LENGTH).decode(FORMAT)
        if message:
            print(f"[{client_addr}] {message}")
            return_msg = RETURN_MSG.encode(FORMAT)
            print(f"[SERVER] returning Message {RETURN_MSG}")
            message_stack.append(return_msg)
        else:
            print(f"[DISCONNECT] {client_addr} disconnecting...")
            message_stack = []
            connected = False
    connection.close()


def send_return(connection):
    while True:
        time.sleep(MSG_WAIT)
        if len(message_stack) > 0:
            connection.send(message_stack.pop(0))


def server_main():
    server.listen()
    global message_stack
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, client_addr = server.accept()
        try:
            # handle_client(connection, client_addr)
            if threading.activeCount() < 2:
                thread_handle_client = threading.Thread(target=handle_client, args=(connection, client_addr))
                thread_send_return = threading.Thread(target=send_return, args=(connection,))
                thread_handle_client.start()
                thread_send_return.start()
        except ConnectionResetError or OSError:
            print(f"[CONNECTION REFUSED] disconnected to client")
            message_stack = []
            thread_handle_client.join()
            thread_send_return.join()
            connection.close()
            continue


print("[STARTING] server is starting...")
server_main()
