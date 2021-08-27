from django.db import models
from django.contrib.auth.models import User


class AWS(models.Model):
    name = models.CharField(
        max_length=10,
        help_text="Enter Account Name"
    )
    account_number = models.CharField(max_length=10, help_text="Enter AWS Account Number")
    region = models.CharField(max_length=10, help_text="Enter AWS Region")
    aws_access_key = models.CharField(max_length=10, help_text="Enter AWS Access Key")
    aws_secret_key = models.CharField(max_length=10, help_text="Enter AWS Secret Key")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

