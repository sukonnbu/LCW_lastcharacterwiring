import socketserver


class RequestHandler(socketserver.BaseRequestHandler):
    users = {}

    def handle(self):
        print("[{}] 접속".format(self.client_address[0]))

        while True:
            self.request.send("채팅 닉네임을 입력하세요".encode())
            user_name = self.request.recv(1024).decode()
            if self.add_user(user_name, self.request, self.client_address):
                break

        while True:
            # bytes
            message = self.request.recv(1024)
            print("[{}]: {}".format(self.client_address[0], message.decode()))

            if message.decode() == "/bye":
                break

            self.send_to_users("[{}]: {}".format(user_name, message.decode()))

        self.delete_user(user_name)

    def add_user(self, user_name, connected_socket, addr):
        if user_name in self.users:
            connected_socket.send("이미 등록된 닉네임입니다.\n".encode())
            return None

        self.users[user_name] = (connected_socket, addr)
        print("현재 참여중: {}명".format(len(self.users)))
        self.send_to_users("[{}] 님이 입장하셨습니다.".format(user_name))

        return user_name

    def delete_user(self, user_name):
        del self.users[user_name]
        print("[{}] 접속 종료\n현재 참여중: {}명".format(self.client_address[0], len(self.users)))
        self.send_to_users("[{}] 님이 퇴장하셨습니다.".format(user_name))
        self.request.close()

    def send_to_users(self, message: str):
        for socket, addr in self.users.values():
            socket.send(message.encode())

    def send_to_all(self, message: str):
        self.send_to_users(message)
        print(message)


class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


chat = ChatServer(("", 8080), RequestHandler)
chat.serve_forever()

chat.shutdown()
chat.server_close()
