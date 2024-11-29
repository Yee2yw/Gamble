import socket
import sys

def recvall(sock, buffer_size=4096):
    """接收完整的数据直到没有更多的数据"""
    data = b''  # 用字节串来存储接收到的数据
    while True:
        part = sock.recv(buffer_size)  # 每次接收 buffer_size 字节
        data += part
        if len(part) < buffer_size:  # 如果接收到的字节少于 buffer_size，说明数据接收完毕
            break
    return data

def host():#游戏规则
        print("欢迎来到骰子游戏!以下是游戏规则\n")
        print("tc:押头彩(两数顺序及点数均正确)>>一赔三十五\n")
        print("tj:押大彩(两数点数正确)>>一赔十七\n")
        print("tp:押空盘(两数不同且均为偶数)>>一赔五\n")
        print("td:押七星(两数之和为七)>>一赔五\n")
        print("te:押头双(两数均为奇数)>>一赔三\n")
        print("ta:押散星(两数之和为3、5、9、11)>>一赔二\n")
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
        host()
        command = input("请输入你的押注命令 (例如 ya tc 10 gold): ")
        client_socket.sendall(command.encode()+b'\r\n')
        print("等待庄家开盘")
        response = recvall(client_socket).decode()
        print(response)

if __name__ == "__main__":
    main()



