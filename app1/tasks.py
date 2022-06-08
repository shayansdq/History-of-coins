from __future__ import absolute_import, unicode_literals
import pandas as pd
import environ
from binance import Client as binance_client
from datetime import datetime
from celery import shared_task
from django_redis import get_redis_connection
import pickle
import zlib
from .utils import *

env = environ.Env()
environ.Env.read_env()
# symbols = env('SYMBOLS').split(',')
exchanges = env('EXCHANGES').split(',')
client = binance_client()
cache = get_redis_connection('default')


# def binance(sy


@shared_task
def get_data(**kwargs):
    candle_data = kwargs['candle_type']
    candle_type = candle_data['type']
    candle_time = candle_data['time']
    print(candle_type, candle_time)
    for exchange in exchanges:
        symbols = env(f'{exchange.upper()}_SYMBOLS').split(',')
        for symbol in symbols:
            last_candles_data = eval(f"{exchange}('{symbol}','{candle_type}','{candle_time}')")
            created_df = eval(f"create_{exchange}_df(last_candles_data)")
            compressed_df = zlib.compress(pickle.dumps(created_df))
            print(created_df)
            cache.set(f"{exchange}-{symbol}-{candle_time}-{candle_type}", compressed_df)
