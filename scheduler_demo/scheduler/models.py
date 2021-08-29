from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class AWS(models.Model):
    name = models.CharField(
        max_length=10,
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
