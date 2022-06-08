# import json
# from datetime import datetime
# from django_redis import get_redis_connection
# import pandas
import pickle
import zlib

# from binance import Client as binance_client, AsyncClient
from django_redis import get_redis_connection
from kucoin.client import Client as kucoin_client
import environ
# from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule
from binance import Client as binance_client
from binance import AsyncClient as async_binance_client
import pandas as pd
import asyncio

cache = get_redis_connection('default')


def create_kucoin_df(candles_data: list):
    """
  [
        "1545904980",             //Start time of the candle cycle
        "0.058",                  //opening price
        "0.049",                  //closing price
        "0.058",                  //highest price
        "0.049",                  //lowest price
        "0.018",                  //Transaction amount
        "0.000945"                //Transaction volume
    ],
    ["""
    separated_pats = list(zip(*candles_data))
    start_times = separated_pats[0]
    open_prices = separated_pats[1]
    close_prices = separated_pats[2]
    highest_prices = separated_pats[3]
    lowest_prices = separated_pats[4]
    transaction_amounts = separated_pats[5]
    transaction_volumes = separated_pats[6]
    data = {
        'start_time': start_times,
        'open_price': open_prices,
        'close_price': close_prices,
        'highest_price': highest_prices,
        'lowest_price': lowest_prices,
        'transaction_amount': transaction_amounts,
        'transaction_volume': transaction_volumes,
    }
    return pd.DataFrame(data)


def create_binance_df(candles_data: list):
    separated_pats = list(zip(*candles_data))
    open_times = separated_pats[0]
    opens = separated_pats[1]
    highs = separated_pats[2]
    lows = separated_pats[3]
    closes = separated_pats[4]
    volumes = separated_pats[5]
    close_times = separated_pats[6]
    quote_asset_volumes = separated_pats[7]
    number_of_trades = separated_pats[8]
    taker_buy_base_asset_volumes = separated_pats[9]
    taker_buy_quote_asset_volumes = separated_pats[10]
    can_be_ignores = separated_pats[11]
    data = {
        'open_time': open_times,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes,
        'close_time': close_times,
        'quote_asset_volume': quote_asset_volumes,
        'number_of_trade': number_of_trades,
        'taker_buy_base_asset_volume': taker_buy_base_asset_volumes,
        'taker_buy_quote_asset_volume': taker_buy_quote_asset_volumes,
        'can_be_ignore': can_be_ignores,
    }
    return pd.DataFrame(data)


async def get_binance_data(client, symbol, candle_type, candle_time):
    last_candles = await async_binance_client().get_klines(symbol=symbol, interval=eval(f"binance_client"
                                                                                        f".KLINE_INTERVAL_"
                                                                                        f"{candle_time}{candle_type}"),
                                                           limit=500)
    print('ok - binance')
    await client.close_connection()
    compressed_df = zlib.compress(pickle.dumps(create_binance_df(last_candles)))
    cache.set(f"binance-{symbol}-{candle_time}-{candle_type}", compressed_df)
    # return create_binance_df(last_candles)


def get_kucoin_data(symbol, candle_type, candle_time):
    import urllib3
    urllib3.disable_warnings()
    match candle_type:
        case 'MINUTE':
            candle_type = 'min'
        case 'HOUR':
            candle_type = 'hour'
        case 'DAY':
            candle_type = 'day'
    client = kucoin_client("api-key", "api-secret", "api-passphrase", False,
                           {"verify": False, "timeout": 20})
    print('ok - kucoin')
    last_candles = client.get_kline_data(symbol, f'{candle_time}{candle_type}', 1507479171)
    last_500_candles = last_candles[-1:-501:-1][::-1]
    return create_kucoin_df(last_500_candles)

# env = environ.Env()
# environ.Env.read_env()

# cache = get_redis_connection('default')
# print('ok')
# print(cache.get('CS_PAIRED_STATUSs'))
# def create_intervals():
#     intervals = env('CANDLES')
#     for candle_type_and_times in intervals.split('.'):
#
#         all_data = candle_type_and_times.split(',')
#
#         candle_type, *times = all_data
#         # candles_data = dict(candle_type=candle_type, times=times)
#         time_type = candle_type.lower()[:-1]
#
#         # print(time_type)
#         for time in times:
#             crontab_type = f"minute='*/{time}',hour='*'" if time_type == 'minute' else f"minute='*',hour='*/{time}'"
#             schedule, _ = eval(f"CrontabSchedule.objects.get_or_create({crontab_type},day_of_week='*',"
#                                f"day_of_month='*',month_of_year='*')")
#             # print(schedule)
#
#             yield candle_type, time, schedule

# #
# def create_tasks():
#     candles_data_and_schedules = create_intervals()
#     # print(list(candles_data_and_schedules))
#     symbols = env('COINS').split(',')
#     print(symbols)
#     exchanges = env('EXCHANGES').split(',')
#     # print(create_intervals())
#     for exchange in exchanges:
#         for symbol in symbols:
#             for data in candles_data_and_schedules:
#                 c_type, time, schedule = data
#                 c_type = c_type[:-1]
#                 # print(c_type, time, schedule)
#                 PeriodicTask.objects.get_or_create(
#                     crontab=schedule,
#                     name=f'{exchange}.{symbol}.{time}.{c_type}',
#                     task=f'app1.tasks.{exchange}',
#                     kwargs=json.dumps({
#                         'symbol': symbol,
#                         'c_type': c_type,
#                         'time': time
#                     }),
#                 )
#

# create_intervals()
# print('ok')
# intervals = env('CANDLES')
# print(intervals)
# create_tasks()
# binance()
# def create_df(candles: list):
