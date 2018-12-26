import pickle
import socket
import random
import threading
import time
import ast
import sys

def println(s):
    print(s)

def diff(a, b):
    return set_dict(DictDiffer(a, b).new_or_changed(), a)

def set_dict(s, d):
    return {k: d[k] for k in s}

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.current_keys.intersection(self.past_keys)

    def added(self):
        """ Find keys that have been added """
        return self.current_keys - self.intersect

    def removed(self):
        """ Find keys that have been removed """
        return self.past_keys - self.intersect

    def changed(self):
        """ Find keys that have been changed """
        return set(o for o in self.intersect
                   if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        """ Find keys that are unchanged """
        return set(o for o in self.intersect
                   if self.past_dict[o] == self.current_dict[o])

    def new_or_changed(self):
        """ Find keys that are new or changed """
        # return set(k for k, v in self.current_dict.items()
        #           if k not in self.past_keys or v != self.past_dict[k])
        return self.added().union(self.changed())


class Client():
    def __init__(self, serverip, serverport, workers=range(0, 2)):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        self.host = s.getsockname()[0]
        s.close()
        # self.host = "127.0.0.1"

        self.new_data = {}

        self.port = 0
        self.server = (serverip,serverport)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.port))
        print(self.server)

        for x in workers:
            threading.Thread(target=self.run, args=(x,)).start()

    def run(self,worker):
        print(worker)
        self.new_data = {}
        while True:
            if worker == 0:
                data, _ = self.receive()
                self.new_data = diff(data, self.new_data)

                list(map(lambda i: println(str(i[0])), list(self.new_data.values())))

                self.new_data = data

            if worker == 1:
                self.send(("{}".format(raw_input()), time.time()))

    def send(self, data):
        d = data
        self.s.sendto(pickle.dumps(d), self.server)

    def receive(self):
        data, addr = self.s.recvfrom(4096)
        return pickle.loads(data), addr

if __name__=="__main__":
    c = Client(str("73.113.154.223"),7005)
    c.start()
