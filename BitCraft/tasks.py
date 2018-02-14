from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from zad.models import CustomerUrl, CustomerFile
from .celery import app

logger = get_task_logger(__name__)


@app.task
@periodic_task(run_every=timedelta(seconds=10))
def DB_clener():
    delta = timezone.now() - timedelta(hours=24)
    CustomerUrl.objects.filter(date__lte=delta).delete
    files = CustomerFile.objects.filter(date__lte=delta)
    if files is not None and len(files) > 0:
        for f in files:
            os.remove('media/' + f.file.name)
        files.delete()



