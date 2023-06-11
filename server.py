import socket

# Create socket and listen on port 5005
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", 5005))
server_socket.listen(5)

# Loop and check for new connections
while 1:
    try:
        client_socket, address = server_socket.accept()
        print(client_socket)

    except socket.timeout:
        continue
    except KeyboardInterrupt:
        server_socket.close()

