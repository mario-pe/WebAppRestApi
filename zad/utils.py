import datetime as idt

import os
from django.contrib.auth.base_user import BaseUserManager
from user_agents import parse

from .models import ActivityArchive, CustomerUrl, CustomerFile


def update_counter(instance):
    instance.counter = instance.counter + 1
    instance.save()


def update_archive_url(instance):
    t = idt.datetime.now()
    archive = ActivityArchive.objects.filter(date=t)
    a = archive.filter().filter().first()
    if a is not None:
        id = instance.id
        new = a.url_activity + str(id) + ","
        a.url_activity = new
        a.save()
    else:
        archive = ActivityArchive()
        id = instance.id
        new = archive.url_activity + str(id)+","
        archive.url_activity = new
        archive.save()


def update_archive_file(instance):
    t = idt.datetime.now()
    archive = ActivityArchive.objects.filter(date=t)
    a = archive.first()
    if a is not None:
        id = instance.id
        new = a.file_activity + str(id) + ","
        a.file_activity = new
        a.save()
    else:
        archive = ActivityArchive()
        id = instance.id
        new = archive.file_activity + str(id)+","
        archive.file_activity = new
        archive.save()


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


def activity_statistcs(urls, files):
    return [len(set(urls.split(','))) - 1, len(set(files.split(','))) - 1]


def daily_statisctic_generator(hours):
    statistic_date = idt.datetime.now() - idt.timedelta(hours=hours)
    archive = ActivityArchive.objects.filter(date=statistic_date).first()
    url = archive.url_activity
    file = archive.file_activity
    clean_archive = activity_statistcs(urls=url, files=file)
    archive.url_activity = clean_archive[0]
    archive.file_activity = clean_archive[1]
    return archive

def daily_statisctic_generator(archive):
    url = archive.url_activity
    file = archive.file_activity
    return [url, file]
