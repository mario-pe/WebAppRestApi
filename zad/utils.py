import datetime as idt

from django.contrib.auth.base_user import BaseUserManager

from .models import ActivityArchive


def update_counter(instance):
    instance.counter = instance.counter + 1
    instance.save()


def update_archive_url(instance):
    t = idt.datetime.now()
    archive = ActivityArchive.objects.filter(date=t)

    if archive is not None:
        a = archive.filter().filter().first()
        id = instance.id
        new = a.url_activity + str(id)+","
        a.url_activity = new
        a.save()
    else:
        archive = ActivityArchive()
        id = instance.id
        new = archive.url_activity + str(id)+","
        archive.url_activity = new
        archive.save()


def fresh_checker(instance):
    instance_date = instance.date.replace(tzinfo=None)
    delta = idt.datetime.now() - idt.timedelta(hours=24)
    print(delta)
    if instance_date > delta:
        return True
    else:
        instance.delete()
        return False


def serializer_saver(serializer):
    instance = serializer.save()
    instance.password = password_generator()
    instance.save()


def password_generator():
    return BaseUserManager().make_random_password()
