# coding: latin-1
import pickle
import socket
import threading
# from urllib3 import urlopen

def println(s):
    print(s)

class Server():
    def __init__(self, port):

        self.clients = []
        self.messages = {}

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        self.host = s.getsockname()[0]
        s.close()
        # self.host = "127.0.0.1"
        # self.host = host

        # port = int(input('Port:'))
        self.port = int(port)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind((self.host,
                     int(port)))

        self.addr = (self.host,self.port)
        print(self.addr)
        threading.Thread(target=self.run, args=(0,)).start()
        threading.Thread(target=self.run, args=(1,)).start()

    def run(self, worker):
        print(worker)
        while True:
            if worker == 0:
                data, addr = self.receive()
                print(data)
                if addr not in self.clients:
                    self.clients.append(addr)

                self.messages[addr] = data

            if worker == 1:
                for client in self.clients:
                    self.send({k: v for k, v in self.messages.items() if k != client}, client)

        s.close()

    def setTimeout(self, seconds):
        self.s.settimeout(seconds)

    def send(self, data, addr):
        self.s.sendto(pickle.dumps(data), addr)

    def receive(self):
        data, addr = self.s.recvfrom(4096)
        return pickle.loads(data), addr
        
if __name__=="__main__":
    # my_ip = urlopen('http://ip.42.pl/raw').read()
    # print("public ip: " + str(my_ip))
    s = Server(host="127.0.0.1", port=7005)
