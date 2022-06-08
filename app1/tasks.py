from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django_redis import get_redis_connection
from .utils import *
import asyncio

env = environ.Env()
environ.Env.read_env()
# symbols = env('SYMBOLS').split(',')
exchanges = env('EXCHANGES').split(',')
# client = binance_client()
api_key = '<api_key>'
api_secret = '<api_secret>'
cache = get_redis_connection('default')


async def binance(candle_data):
    exchange = 'binance'
    symbols = env(f'{exchange.upper()}_SYMBOLS').split(',')
    candle_type = candle_data['type']
    candle_time = candle_data['time']
    client = await async_binance_client.create(api_key, api_secret)
    await asyncio.gather(*[get_binance_data(client, symbol, candle_type, candle_time) for symbol in symbols])
    # await asyncio.gather(*[kucoin(client, symbol, candle_type, candle_time) for symbol in symbols])
    await client.close_connection()


def kucoin(candle_data):
    candle_type = candle_data['type']
    candle_time = candle_data['time']
    kucoin_symbols = env('KUCOIN_SYMBOLS').split(',')
    for symbol in kucoin_symbols:
        created_df = get_kucoin_data(symbol, candle_type, candle_time)
        compressed_df = zlib.compress(pickle.dumps(created_df))
        cache.set(f"kucoin-{symbol}-{candle_time}-{candle_type}", compressed_df)


@shared_task
def get_data(**kwargs):
    candle_data = kwargs['candle_type']
    asyncio.run(binance(candle_data))
    kucoin(candle_data)
