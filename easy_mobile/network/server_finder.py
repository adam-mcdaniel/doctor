import socket, time

def label(data):
    split_data = data.split(":")
    labeled_data = {
                    "ip":   split_data[0],
                    "port": split_data[1],
                    "game": split_data[2],
                    "room": split_data[3]
                    }
    return labeled_data

class ServerFinder():
    def __init__(self, port=7000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", port))
        self.client.settimeout(0.2)

        self.available_servers = []

    def refresh(self):
        try:
            for x in range(50):
                data, addr = self.client.recvfrom(1024)
                labeled_data = label(data)
                if labeled_data not in self.available_servers:
                    self.available_servers.append(labeled_data)
        except:
            pass

    def getAvailableServers(self):
        return self.available_servers

    def getRoom(self, room):
        for server in self.getAvailableServers():
            if server["room"] == room:
                return server

    def close(self):
        self.client.close()


if __name__ == "__main__":
    sf = ServerFinder(7000)
    sf.refresh()

    print(sf.getAvailableServers())
