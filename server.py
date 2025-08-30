from socket import socket
from struct import unpack

ACK = "ACK!"

ACTION = "rb"

THANK_YOU_FOR_ASKING_ = "Hey client I'm good, thank you for asking!"

BUFSIZE = 1024

FORMAT = "!I"

BACKLOG = 1

IP = "127.0.0.1"

PORT = 8200

class ServerHttp:
    def __init__(self,ip,port,backlog):
        self.ip=ip
        self.port=port
        self.backlog=backlog

    def open_main_socket(self) -> socket:
        """open and return the main socket->from him, we'll do client_socket"""
        main_socket = socket()
        main_socket.bind((self.ip, self.port))
        main_socket.listen(self.backlog)
        print("Main socket has opened!")
        return main_socket

    def read_file(self,file_name) -> bytes:
        """Read from the file_name that I got from the client the content"""
        with open(file_name, ACTION) as file:
            return file.read()

    def handle_file(self,user_socket):
        """Take the name of the file and use read_file function for take the content of the file"""
        file_name = user_socket.recv(BUFSIZE).decode()
        print("Get the file name from the client!")
        content_file = self.read_file(file_name)
        user_socket.send(content_file)
        print("Send the server the content of the file-> the client download the content! ")

    def handle_cases(self,user_socket):
        """handle with the 3 cases 1-exit 2-download file 3-how is the server"""
        recv_data = unpack(FORMAT, user_socket.recv(BUFSIZE))[0]
        while recv_data:
            if recv_data!=1:
                #I cant send ack when the client ended communication
                user_socket.send(ACK.encode())
            if recv_data == 1:
                print("Ended communication and close sockets-> server side!")
                break

            elif recv_data == 2:
                self.handle_file(user_socket)

            elif recv_data == 3:
                user_socket.send(THANK_YOU_FOR_ASKING_.encode())
                print("Sent OK message to the client!")
            recv_data = unpack(FORMAT, user_socket.recv(BUFSIZE))[0]

    def manage_socket(self):
        """manage the socket open and close-> the main function of the system"""
        main_socket = self.open_main_socket()
        user_socket, addr = main_socket.accept()
        print(f"opened user socket {addr}")

        self.handle_cases(user_socket)

        main_socket.close()
        user_socket.close()

def main():
    http_server=ServerHttp(IP,PORT,BACKLOG)
    http_server.manage_socket()

if __name__=="__main__":
    main()