import socket
import threading
import random

from util import recv_all


class DiceGameServer:
    """
    骰子游戏服务器类，用于管理客户端连接和处理押注命令。
    
    参数:
    - host (str): 服务器IP地址，默认为 '127.0.0.1'
    - port (int): 服务器端口号，默认为 12345
    """

    def __init__(self, host='0.0.0.0', port=12345, client_num=2):
        self.host = host
        self.port = port
        self.clients = []
        self.client_msg = {}
        self.clientNums = client_num
        self.readyNums = 0
        self.readyFlag = False
        self.dice = [0, 0]
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
            data = recv_all(client_socket)
            if data == 'exit':
                client_socket.close()
                self.clients.remove(client_socket)
                break
            self.readyNums += 1
            if self.readyNums >= self.clientNums:
                self.new_round()
                self.readyFlag = True
            while not self.readyFlag:
                pass
            response = self.process_command(data)
            client_socket.sendall(response.encode())
            self.readyNums -= 1
            self.readyFlag = False

    def new_round(self):
        self.dice = [random.randint(1, 6), random.randint(1, 6)]

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

        result_message = f"庄家叫道：{self.dice[0]}、{self.dice[1]}……"
        win_amount = 0

        if bet_type == 'tc' and self.dice[0] + self.dice[1] == 7 and abs(self.dice[0] - self.dice[1]) == 5:
            win_amount = amount * 35
            result_message += " 头彩！"
        elif bet_type == 'dc' and (self.dice[0] + self.dice[1] == 7 or abs(self.dice[0] - self.dice[1]) == 5):
            win_amount = amount * 17
            result_message += " 大彩！"
        elif bet_type == 'kp' and self.dice[0] % 2 == 0 and self.dice[1] % 2 == 0 and self.dice[0] != self.dice[1]:
            win_amount = amount * 5
            result_message += " 空盘！"
        elif bet_type == 'qx' and self.dice[0] + self.dice[1] == 7:
            win_amount = amount * 5
            result_message += " 七星！"
        elif bet_type == 'dd' and self.dice[0] % 2 == 1 and self.dice[1] % 2 == 1:
            win_amount = amount * 3
            result_message += " 单对！"
        elif bet_type == 'sx' and self.dice[0] + self.dice[1] in [3, 5, 9, 11]:
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
