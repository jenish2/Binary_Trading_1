# Author : Jenish Dholariya
import pandas as pd
from iqoptionapi.stable_api import IQ_Option


class BrokerIqOption:
    def __init__(self, credentials: dict, balance_type):
        self.IQ = None
        self.EMAIL = credentials['user_email']
        self.PASSWORD = credentials['password']
        self.BALANCE_TYPE = balance_type  # PRACTICE / REAL / TOURNAMENT

    def connect(self):
        iq = IQ_Option(self.EMAIL, self.PASSWORD)
        check, reason = iq.connect()
        if check:
            print("\nSuccessfully logged in account!!\n")
            self.IQ = iq
            self.IQ.change_balance(self.BALANCE_TYPE)
        else:
            while True:
                if not iq.check_connect():
                    print("Trying reconnect!")
                    check, reason = iq.connect()
                    if check:
                        print("\nSuccessfully logged in account!!\n")
                        return iq()
                    else:
                        print("\nFailed login due to  below reason:-")
                        print(reason)
                        print()
                else:
                    self.IQ = iq
                    self.IQ.change_balance(self.BALANCE_TYPE)

    def get_candle_data(self, goal: str, timeframe_of_chart_in_minute: int):
        timestamp = self.IQ.get_server_timestamp()
        candle = []
        for _ in range(6):
            x = self.IQ.get_candles(goal, (timeframe_of_chart_in_minute * 60), 1000, timestamp)
            timestamp = int(x[0]["from"]) - 1
            candle += x

        dataframe = pd.DataFrame(candle)
        dataframe.sort_values(by=["from"], inplace=True, ascending=True)
        dataframe.drop(dataframe.tail(1).index, inplace=True)
        print("data fetched by api")
        return dataframe[["from", "close", "min", "max", "volume"]]

    def place_order(self, goal, amount, action, duration):
        order, order_id = self.IQ.buy_digital_spot(active=goal, amount=amount, action=action, duration=duration)
        if order:
            print(
                "Order placed successfully with orderid:- {}    amount:- {}     action:- {}     duration:- {} min".format(
                    order_id,
                    amount,
                    action,
                    duration))
        else:
            print("order failed!!")
            print(order_id)
        return order, order_id

    @property
    def balance(self):
        return self.IQ.get_balance()


if __name__ == "__main__":
    cred = {
        "user_email": "rolimiw174@vpsrec.com",
        "password": "Abc@123@Xyz"
    }

    biq = BrokerIqOption(credentials=cred, balance_type="PRACTICE")
    biq.connect()
    print(biq.get_candle_data(goal="EURUSD-OTC", timeframe_of_chart_in_minute=5))
    print(biq.balance)
    biq.place_order(goal="EURUSD-OTC", amount=1, action="call", duration=1)
