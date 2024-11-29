import socket


def recv_all(sock: socket.socket):
    data = b''
    while True:
        part = sock.recv(1024)
        data += part
        if part.endswith(b'\r\n'):
            break
    return data.decode('utf-8').rstrip('\r\n')
