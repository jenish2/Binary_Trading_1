# Author : Jenish Dholariya
import time
from datetime import datetime
from threading import Thread

import pytz

from Bot.entry_condition_check import EntryConditionCheck
from Broker.broker_api import BrokerIqOption


class Bot(Thread):
    def __init__(self, credentials, configuration):
        Thread.__init__(self, daemon=False)
        self.CRED = credentials
        self.CONFIG = configuration
        self.API = BrokerIqOption(credentials=self.CRED, balance_type=self.CONFIG['account_mode'])
        self.API.connect()

    @staticmethod
    def tick_on_timeframe(timeframe_of_chart_in_minute: int):
        cT = datetime.now(pytz.timezone('UTC'))
        return (cT.second == 0) and (cT.minute % timeframe_of_chart_in_minute == 0)

    def run(self) -> None:
        while True:
            try:
                if self.tick_on_timeframe(self.CONFIG['timeframe_of_chart_in_minute']):
                    try:
                        for watch in self.CONFIG['watchlist']:
                            time.sleep(2)
                            df = self.API.get_candle_data(watch['goal'], self.CONFIG['timeframe_of_chart_in_minute'])
                            can_enter, entry_action = EntryConditionCheck.check_for_entry(df, self.CONFIG)
                            if can_enter:
                                order_status, order_id = self.API.place_order(watch['goal'],
                                                                              self.CONFIG['amount_for_trade'],
                                                                              entry_action,
                                                                              self.CONFIG['duration'])


                    except Exception as e:
                        print("Inner First For Loop")
                        print(e)
                        continue

            except Exception as e:
                print("Out side of the loop")
                print(e)
                continue
