from __future__ import absolute_import, unicode_literals

from datetime import timedelta
import datetime as idt

import os
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from zad.utils import activity_statistcs, daily_statisctic_generator
from .celery import app
from zad.models import CustomerUrl, CustomerFile, ActivityArchive

logger = get_task_logger(__name__)


@app.task
@periodic_task(run_every=timedelta(seconds=10))
def DB_clener():

    delta = idt.datetime.now() - idt.timedelta(hours=24)
    CustomerUrl.objects.filter(date__lte=delta).delete
    files = CustomerFile.objects.filter(date__lte=delta)
    if files is not None and len(files) > 0:
        for f in files:
            os.remove('media/' + f.file.name)
        files.delete()


@app.task
@periodic_task(run_every=timedelta(hours=24))
def statistic():
    archive = daily_statisctic_generator(hours=24)
    archive.save()


