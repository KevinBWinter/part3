import socket
import threading
import os
import signal
import sys
import time


connection_count = 0


def handle_client(conn, addr):
    global connection_count
    connection_count += 1
    connection_id = connection_count
    
    print(f"Connection {connection_id} from {addr}")

    # Receive data from the client
    data = conn.recv(1024)
    received_data = b""
    timeout = 10  # Timeout in seconds
    start_time = time.time()

    while data:
        received_data += data
        # Set a timeout for receiving data
        conn.settimeout(timeout - (time.time() - start_time))
        try:
            data = conn.recv(1024)
        except socket.timeout:
            # Timeout reached, close the connection
            print(f"Connection {connection_id} timed out")
            conn.close()
            return

 
    filename = f"{connection_id}.file"
    file_path = os.path.join(FILE_DIR, filename)
    with open(file_path, 'wb') as file:
        file.write(received_data)

    print(f"File saved as {filename}")
    conn.close()


def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 server.py <PORT> <FILE-DIR>")
        sys.exit(1)

    PORT = int(sys.argv[1])
    FILE_DIR = sys.argv[2]

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(10)
    print(f"Server listening on port {PORT}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
