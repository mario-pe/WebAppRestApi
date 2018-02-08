from django.contrib import admin
from .models import *


class CustomerUrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'password', 'date')


class CustomerFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'password', 'date')


class ActivityArchiveAdmin(admin.ModelAdmin):
    list_display = ('date', 'url_activity', 'file_activity')


admin.site.register(CustomerUrl, CustomerUrlAdmin)
admin.site.register(CustomerFile, CustomerFileAdmin)
admin.site.register(ActivityArchive, ActivityArchiveAdmin)