# from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .utils import *
# executes every 10 seconds.
# schedule, created = IntervalSchedule.objects.get_or_create(
#     every=10,
#     period=IntervalSchedule.SECONDS,
# )
# PeriodicTask.objects.get_or_create(
#     interval=schedule,  # we created this above.
#     name='Importing contacts',  # simply describes this periodic task.
#     task='app1.tasks.get_history',  # name of task.
# )
# print('ok')
