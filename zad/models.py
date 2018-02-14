from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse
from django import utils


class CustomerUrl(models.Model):
    url = models.TextField()
    password = models.CharField(max_length=15)
    date = models.DateTimeField(default=utils.timezone.now)
    counter = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.url, self.password, self.date, self.counter)

    def get_absolute_url(self):
        return reverse("zad:customer_url_details", kwargs={"id": self.id})


class CustomerFile(models.Model):
    file = models.FileField(upload_to="Doc/", default='Doc/None/no-doc.pdf')
    password = models.CharField(max_length=15)
    date = models.DateTimeField(default=utils.timezone.now)
    counter = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.password, self.date, self.counter)

    def get_absolute_url(self):
        return reverse("zad:customer_file_details", kwargs={"id": self.id})

