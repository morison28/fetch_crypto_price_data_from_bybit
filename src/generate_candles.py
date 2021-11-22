import argparse
from datetime import timedelta, timezone
import os

import pandas as pd
from tqdm import tqdm
from rich import print

from fetch_executions_from_bybit import create_date_list


def generate_candles(df_exec, period):
    """ period間隔のローソク足を作成
    Args:
      df_exec: 約定データCSV
      period(str): 時間間隔
    Return:
      df_candle
    """
    df_exec['exec_date'] = pd.to_datetime(df_exec['timestamp']*1000000000)
    # 売買別で出来高を記録
    df_exec['volume'] = df_exec['size']
    df_exec['buy_volume'] = df_exec['volume'].where(df_exec['side']=='Buy', 0)
    df_exec['sell_volume'] = df_exec['volume'].where(df_exec['side']=='Sell', 0)
    # 売買別カウント
    df_exec['count'] = 1
    df_exec['buy_count'] = df_exec['count'].where(df_exec['side']=='Buy', 0)
    df_exec['sell_count'] = df_exec['count'].where(df_exec['side']=='Sell', 0)
    # 売買別約定量
    df_exec['value'] = df_exec['price'] * df_exec['size']
    df_exec['buy_value'] = df_exec['value'].where(df_exec['side']=='Buy', 0)
    df_exec['sell_value'] = df_exec['value'].where(df_exec['side']=='Sell', 0)
    df_candle = df_exec.set_index('exec_date').resample(period).agg({
        'price': 'ohlc',
        'volume': 'sum',
        'buy_volume': 'sum',
        'sell_volume': 'sum',
        'count': 'sum',
        'buy_count': 'sum',
        'sell_count': 'sum',
        'value': 'sum',
        'buy_value': 'sum',
        'sell_volume': 'sum'})
    df_candle.columns = df_candle.columns.droplevel()
    df_candle.index = df_candle.index + timedelta(hours=9)
    df_candle = df_candle.tz_localize(timezone(timedelta(hours=9), 'JST'))
    return df_candle

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", type=str)
    parser.add_argument("start_date", type=str)
    parser.add_argument("end_date", type=str)
    parser.add_argument("period", type=str)
    args = parser.parse_args()

    date_list = create_date_list(args.start_date, args.end_date)
    dfs = []
    for date in tqdm(date_list):
        executions_file = f"../data/bybit/executions/{args.symbol}/{args.symbol}{date}.pickle"
        df_exec = pd.read_pickle(executions_file)
        df_candles = generate_candles(df_exec, args.period)
        dfs.append(df_candles)
    df_all_candles = pd.concat(dfs)
    if  not args.symbol in os.listdir("../data/bybit/candles/"):
        os.mkdir(f"../data/bybit/candles/{args.symbol}")
    df_all_candles.to_pickle(f"../data/bybit/candles/{args.symbol}/{args.symbol}_{args.period}_{df_all_candles.index[0]}-{df_all_candles.index[-1]}.pickle")
    
    



