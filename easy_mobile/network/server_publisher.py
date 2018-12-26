import threading
import socket
import time

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

class ServerPublisher():
    def __init__(self, ip="127.0.0.1", port=0, name="", room=""):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server.settimeout(0.2)
        self.server.bind(("", 0))
        self.port = port
        self.message = b"{}:{}:{}:{}".format(ip, port, name, room)
        threading.Thread(target=self.publish, args=()).start()

    def publish(self):
        while True:
            self.server.sendto(self.message, ('<broadcast>', self.port))
            time.sleep(0.02)

    def close(self):
        self.server.close()

if __name__ == "__main__":
    ServerPublisher(getIP(), 8080, "Cards!", 0)
    print("Server instantiated!")