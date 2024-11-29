import socket
import threading
import random

class DiceGameServer:
    """
    骰子游戏服务器类，用于管理客户端连接和处理押注命令。
    
    参数:
    - host (str): 服务器IP地址，默认为 '127.0.0.1'
    - port (int): 服务器端口号，默认为 12345
    """
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def broadcast(self, message):
        """
        广播消息给所有连接的客户端。
        
        参数:
        - message (str): 要广播的消息
        """
        for client in self.clients:
            try:
                client.sendall(message.encode())
            except:
                client.close()
                self.clients.remove(client)

    def handle_client(self, client_socket):
        """
        处理单个客户端的连接和通信。
        
        参数:
        - client_socket (socket): 客户端套接字
        """
        while True:
            try:
                data = client_socket.recv(1024).decode().strip()
                if not data:
                    break
                response = self.process_command(data)
                client_socket.sendall(response.encode())
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        client_socket.close()
        self.clients.remove(client_socket)

    def process_command(self, command):
        """
        处理客户端发送的押注命令并返回结果。
        
        参数:
        - command (str): 客户端发送的押注命令
        
        返回:
        - str: 押注结果的响应消息
        """
        parts = command.split()
        if len(parts) < 3 or parts[0] != 'ya':
            return "Invalid command format"

        bet_type = parts[1]
        amount = int(parts[2])
        currency = parts[3]

        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

        result_message = f"庄家叫道：{dice1}、{dice2}……"
        win_amount = 0

        if bet_type == 'tc' and dice1 + dice2 == 7 and abs(dice1 - dice2) == 5:
            win_amount = amount * 35
            result_message += " 头彩！"
        elif bet_type == 'dc' and (dice1 + dice2 == 7 or abs(dice1 - dice2) == 5):
            win_amount = amount * 17
            result_message += " 大彩！"
        elif bet_type == 'kp' and dice1 % 2 == 0 and dice2 % 2 == 0 and dice1 != dice2:
            win_amount = amount * 5
            result_message += " 空盘！"
        elif bet_type == 'qx' and dice1 + dice2 == 7:
            win_amount = amount * 5
            result_message += " 七星！"
        elif bet_type == 'dd' and dice1 % 2 == 1 and dice2 % 2 == 1:
            win_amount = amount * 3
            result_message += " 单对！"
        elif bet_type == 'sx' and dice1 + dice2 in [3, 5, 9, 11]:
            win_amount = amount * 2
            result_message += " 散星！"
        else:
            result_message += " 庄家赢了！"

        result_message += f"\n你{'赢' if win_amount > 0 else '输'}了 {abs(win_amount)} {currency}。\n"
        return result_message

    def start(self):
        """
        启动服务器，监听客户端连接并创建处理线程。
        """
        print("Server started on {}:{}".format(self.host, self.port))
        while True:
            client_socket, addr = self.server_socket.accept()
            print("Connected by", addr)
            self.clients.append(client_socket)
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start()

if __name__ == "__main__":
    server = DiceGameServer()
    server.start()