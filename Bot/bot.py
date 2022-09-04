# Author : Jenish Dholariya
from threading import Thread

from Broker.broker_api import BrokerIqOption


class Bot(Thread):
    def __init__(self, credentials, configuration):
        self.CRED = credentials
        self.CONFIG = configuration
        self.API = BrokerIqOption(credentials=self.CRED, balance_type=self.CONFIG['account_mode'])
        self.API.connect()

    def run(self) -> None:
        pass
