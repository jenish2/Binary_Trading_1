import pandas as pd
import talib as ta


class EntryConditionCheck:
    @staticmethod
    def check_for_entry(df: pd.DataFrame, config: dict):
        print("checking for entry condition")
        current_close = df['close'].iat[-1]
        df.drop(df.tail(1).index, inplace=True)
        df['BBANDS_U'], df['BBANDS_M'], df['BBANDS_L'] = ta.BBANDS(
            df[config['bollinger_band']['source']],
            timeperiod=config['bollinger_band']['length'],
            nbdevup=config['bollinger_band'][
                'standard_deviation'])

        if current_close >= (df['BBANDS_U'].iat[-1] * (1 + (config['x_%_value'] / 100))):
            if not config['reverse_condition']:
                return True, 'put'
            else:
                return True, 'call'

        if current_close <= (df['BBANDS_L'].iat[-1] * (1 - (config['y_%_value'] / 100))):
            if not config['reverse_condition']:
                return True, 'call'
            else:
                return True, 'put'

        return False, ""
