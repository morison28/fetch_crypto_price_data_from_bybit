
import argparse
from datetime import datetime, timedelta, timezone
import os
import sys

import gzip
import pandas as pd
from rich import print
from tqdm import tqdm
import urllib.request

# 約定データ
# 期間
# ペア

# ローソク
# どの時間軸

# argparser使う？
# shell書く？

BASE_URL = "https://public.bybit.com/trading/"
DIR = "../data/bybit/executions/"

def download_url(url:str,zipfile_path:str):
    """ {url}先の約定データzipを{zipfile_path}に保存 """
    with urllib.request.urlopen(url) as dl_file:
        with open(zipfile_path, 'wb') as out_file:
            out_file.write(dl_file.read())

def create_date_list(start_date:str,end_date:str) -> list:
    """ 文字列型の日付リストを作成 """
    # TODO: 存在しない日付を入力してもエラーで止まらない様にする
    try:
        datetime_format = '%Y-%m-%d'
        start = datetime.strptime(start_date, datetime_format)
        end = datetime.strptime(end_date, datetime_format)
        period = (end - start).days
        return [datetime.strftime(start+timedelta(i),datetime_format) for i in range(period+1)]
    except:
        print('error: startdate or end_date out of month range')

def fetch_executions_from_bybit(symbol:str, start_date:str, end_date:str):
    """ bybit
    Parameters:
    ----------
    symbol:

    Returns:
    ----------
    """
    save_dir = f"../data/bybit/executions/{symbol}/"
    if not symbol in os.listdir("../data/bybit/executions/"):
        os.mkdir(save_dir)

    target_date_list = create_date_list(start_date, end_date)
    for date in tqdm(target_date_list):
        file_name = f"{symbol}{date}.pickle"
        file_path = f"{save_dir}{file_name}"
        zipfile_name = f"{symbol}{date}.csv.gz"
        if not file_name in os.listdir(save_dir):
            download_url(f"https://public.bybit.com/trading/{symbol}/{zipfile_name}", zipfile_name)
            pd.read_csv(zipfile_name).to_pickle(file_path)
            os.remove(zipfile_name)
        else:
            # target executions data file is already exist ..
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", type=str)
    parser.add_argument("start_date", type=str)
    parser.add_argument("end_date", type=str)
    args = parser.parse_args()
    fetch_executions_from_bybit(args.symbol, args.start_date, args.end_date)







