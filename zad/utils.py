import datetime as idt

import os
from django.contrib.auth.base_user import BaseUserManager
from user_agents import parse

from .models import CustomerUrl, CustomerFile


def update_counter(instance):
    instance.counter = instance.counter + 1
    instance.save()


def db_clener():
    delta = idt.datetime.now() - idt.timedelta(hours=24)
    CustomerFile.objects.filter(date__lte=delta).delete
    files = CustomerUrl.objects.filter(date__lte=delta)
    if files is not None and len(files) > 0:
        for f in files:
            os.remove('media/' + f.file.name)
        files.delete()


def user_agent_support(request):
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    request.session['user_agent'] = user_agent.__str__()


def serializer_saver(serializer):
    instance = serializer.save()
    instance.password = password_generator()
    instance.save()


def password_generator():
    return BaseUserManager().make_random_password()






