import sys
import socket
import signal
import threading

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if len(sys.argv) != 3:
    sys.stderr.write("ERROR: Incorrect number of arguments\n")
    sys.exit(1)

try:
    port = int(sys.argv[1])
except ValueError:
    sys.stderr.write("ERROR: Invalid port number\n")
    sys.exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', port))
server_socket.listen()

def handle_client(client_socket, connection_id):
    client_socket.sendall(b'accio\r\n')
    data = client_socket.recv(1024)
    if not data:
        with open(f'{connection_id}.file', 'wb') as file:
            file.write(b'ERROR')
    else:
        with open(f'{connection_id}.file', 'wb') as file:
            file.write(data)
    client_socket.close()

connection_counter = 0
while True:
    client_socket, _ = server_socket.accept()
    connection_counter += 1
    threading.Thread(target=handle_client, args=(client_socket, connection_counter)).start()

