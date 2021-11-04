import time
from datetime import datetime, timedelta
from random import randint
from threading import Thread, Timer

from faker import Faker

fkr = Faker()


class ConnectionChecker:
    """
    This class checks if user's connection is stale and should be deleted
    """
    def check_connections(self):
        print("Check Connection")
        for socket, last_active in self.clients.items():
            if datetime.now() - last_active > timedelta(seconds=3):
                print(f'Connection {socket} is stale')
                del self.clients[socket]
        timer = Timer(interval=1.0, function=self.check_connections)
        timer.start()


class Connector(ConnectionChecker):
    def __init__(self):
        self.clients = {}
        self.check_connections()

    def create_user_connection(self, client):
        print(f'Connection {client.socket} created')
        self.clients[client.socket] = datetime.now()


class Client:
    def __init__(self, connector):
        super().__init__()
        self.ip = fkr.ipv4()
        self.port = randint(1000, 9999)
        self.socket = self.ip, self.port
        self.connector = connector
        self.connector.create_user_connection(self)

    def update_status(self):
        while True:
            time.sleep(randint(1, 6))
            self.connector.clients[self.socket] = datetime.now()


def main_loop():
    connector = Connector()
    while True:
        client = Client(connector=connector)
        th = Thread(target=client.update_status)
        th.start()
        time.sleep(randint(1, 5))


if __name__ == '__main__':
    main_loop()
