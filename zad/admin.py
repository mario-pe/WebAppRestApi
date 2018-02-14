from django.contrib import admin
from .models import *


class CustomerUrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'password', 'date')


class CustomerFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'password', 'date')



admin.site.register(CustomerUrl, CustomerUrlAdmin)
admin.site.register(CustomerFile, CustomerFileAdmin)
