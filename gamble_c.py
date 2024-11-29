import socket
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: gamble_c.py <ServerIP>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    print("Connected to the server.")

    while True:
        command = input("请输入你的押注命令 (例如 ya tc 10 gold): ")
        client_socket.sendall(command.encode())

        response = client_socket.recv(1024).decode()
        print(response)

if __name__ == "__main__":
    main()



