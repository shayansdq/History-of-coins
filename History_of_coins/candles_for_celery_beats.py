from celery.schedules import crontab
from pathlib import Path
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

candles = {
    '1_minute_candle': {
        'task': 'app1.tasks.get_data',
        'schedule': crontab(minute='*/1'),
        'kwargs': {
            'candle_type':
                {
                    'type': 'MINUTE',
                    'time': 1
                }
        },
    },
    '5_minute_candle': {
        'task': 'app1.tasks.get_data',
        'schedule': crontab(minute='*/5'),
        'kwargs': {
            'candle_type':
                {
                    'type': 'MINUTE',
                    'time': 5
                }
        },
    },
    '15_minute_candle': {
        'task': 'app1.tasks.get_data',
        'schedule': crontab(minute='*/15'),
        'kwargs': {
            'candle_type':
                {
                    'type': 'MINUTE',
                    'time': 15
                }
        },
    },
    '30_minute_candle': {
        'task': 'app1.tasks.get_data',
        'schedule': crontab(minute='*/30'),
        'kwargs': {
            'candle_type':
                {
                    'type': 'MINUTE',
                    'time': 30
                }
        },
    },
    '1_hour_candle': {
        'task': 'app1.tasks.get_data',
        'schedule': crontab(minute='0'),
        'kwargs': {
            'candle_type':
                {
                    'type': 'HOUR',
                    'time': 1
                }
        },
    },
    '4_hour_candle': {
        'task': 'app1.tasks.get_data',
        'schedule': crontab(hour='*/4',minute='0'),
        'kwargs': {
            'candle_type':
                {
                    'type': 'HOUR',
                    'time': 4
                }
        },
    },
    '1_daily_candle': {
        'task': 'app1.tasks.get_data',
        'schedule': crontab(hour='*/24',minute='0'),
        'kwargs': {
            'candle_type':
                {
                    'type': 'DAY',
                    'time': 1
                }
        },
    }
}
