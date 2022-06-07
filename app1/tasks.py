from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def add(**kwargs):
    print(kwargs['coins'])
    print(type(kwargs['coins']))
    # return coins, candle_type
