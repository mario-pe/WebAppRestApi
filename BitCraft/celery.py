from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BitCraft.settings')
app = Celery('tasks',
             broker='amqp://',
             backend='amqp://',
             include=['BitCraft.tasks'])


app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()