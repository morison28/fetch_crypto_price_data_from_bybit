
import argparse
from datetime import datetime, timedelta
import os
from typing import List

import gzip
import pandas as pd
from tqdm import tqdm
import urllib.request
from urllib.error import URLError, HTTPError


BASE_URL = "https://public.bybit.com/trading/"

class InvalidDateFormat(Exception):
    """ Raise when an invalid date format is specified """
    pass

class InvalidDateRange(Exception):
    """ Raise when an invald date range is specified """
    pass

def download_url(url:str, zipfile_path:str):
    """
    Download a file from the specified URL and save it to the specified path.

    Args:
        url (str): The URL of the file to download.
        zipfile_path (str): The path where the download file will be saved.

    Raises:
        URLError: If there is an error in the URL.
        HTTPError: If there is an error in the HTTP request.
        IOError: If there is an error in the I/O operation.
    """
    try:
        with urllib.request.urlopen(url) as dl_file:
            with open(zipfile_path, 'wb') as output_file:
                output_file.write(dl_file.read())
    except URLError as e:
        raise URLError(f"Could not connect to {url}") from e
    except HTTPError as e:
        raise HTTPError(f"HTTP error occurred while connecting to {url}") from e
    except IOError as e:
        raise IOError(f"Could not write file to {zipfile_path}") from e

def create_date_list(start_date:str,end_date:str) -> List[str]:
    """ 
    Create a list of dates in string format.

    Args:
        start_date (str): Start date in the format "YYYY-MM-DD"
        end_date (str): End date in the format "YYYY-MM-DD"

    Returns:
        A list of dates between start_date adn end_date (inclusive).
    """
    datetime_format = '%Y-%m-%d'
    try:
        start = datetime.strptime(start_date, datetime_format)
        end = datetime.strptime(end_date, datetime_format)
    except ValueError:
        InvalidDateFormat('Invalid date format. Use "YYYY-MM-DD"')
    if start > datetime.now() or end > datetime.now():
        raise InvalidDateRange('Invalid date range. Cannot specify a future date.')
    if start > end:
        raise InvalidDateRange('Start date is later than end date')
    delta = end - start
    date_list = [datetime.strftime(start + timedelta(i), datetime_format) for i in range(delta.days+1)]
    return date_list

def fetch_executions_from_bybit(symbol:str, start_date:str, end_date:str, save_dir:str):
    """
    
    """
    target_date_list = create_date_list(start_date, end_date)
    for date in tqdm(target_date_list):
        file_name = f"{symbol}{date}.pickle"
        file_path = f"{save_dir}{file_name}"
        zipfile_name = f"{symbol}{date}.csv.gz"
        if not file_name in os.listdir(save_dir):
            download_url(f"{BASE_URL}{symbol}/{zipfile_name}", zipfile_name)
            pd.read_csv(zipfile_name).to_pickle(file_path)
            os.remove(zipfile_name)
        else:
            # target executions data file is already exist ..
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--start_date", type=str, required=True)
    parser.add_argument("--end_date", type=str, required=True)
    parser.add_argument("--save_dir", type=str, required=True)
    args = parser.parse_args()
    save_dir = args.save_dir if args.save_dir[-1]=='/' else args.save_dir + '/'
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fetch_executions_from_bybit(args.symbol, args.start_date, args.end_date, save_dir)