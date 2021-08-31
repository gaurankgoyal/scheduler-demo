from django.contrib import admin
from .models import AWS, CronJob

# Register your models here.
admin.site.register(AWS)
admin.site.register(CronJob)