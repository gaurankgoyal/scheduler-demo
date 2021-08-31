from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class AWS(models.Model):
    name = models.CharField(
        max_length=30,
        help_text="Enter Account Name"
    )
    account_number = models.CharField(max_length=12, help_text="Enter AWS Account Number")
    region = models.CharField(max_length=16, help_text="Enter AWS Region")
    aws_access_key = models.CharField(max_length=20, help_text="Enter AWS Access Key")
    aws_secret_key = models.CharField(max_length=40, help_text="Enter AWS Secret Key")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('accounts')


class CronJob(models.Model):
    name = models.CharField(
        max_length=30,
        help_text="Enter a Cron Job Name"
    )
    start_cronjob = models.CharField(
        max_length=30,
        help_text="Enter Cron Job for the scheduler eg '* * * ? * *'"
    )
    stop_cronjob = models.CharField(
        max_length=30,
        help_text="Enter Cron Job for the scheduler eg '* * * ? * *'"
    )
    instance_id = models.CharField(
        max_length=80,
        help_text="Instance Id"
    )
    aws_name_start = models.CharField(
        max_length=200,
        help_text="AWS Name for Cron Job",
        default="aws"
    )
    aws_name_stop = models.CharField(
        max_length=200,
        help_text="AWS Name for Cron Job",
        default="aws"
    )
    account = models.ForeignKey(AWS, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
