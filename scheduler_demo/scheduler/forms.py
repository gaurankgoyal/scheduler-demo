from django import forms
from django.forms import ModelForm
from .models import AWS


AWS_REGION= [
    ("us-east-2", "US East (Ohio)"),
    ("us-east-1", "US East (N. Virginia)"),
    ("us-west-1", "US West (N. California)"),
    ("us-west-2", "US West (Oregon)"),
    ("af-south-1", "Africa (Cape Town)"),
    ("ap-east-1", "Asia Pacific (Hong Kong)"),
    ("ap-south-1", "Asia Pacific (Mumbai)"),
    ("ap-northeast-3", "Asia Pacific (Osaka)"),
    ("ap-northeast-2", "Asia Pacific (Seoul)"),
    ("ap-southeast-1", "Asia Pacific (Singapore)"),
    ("ap-southeast-2", "Asia Pacific (Sydney)"),
    ("ap-northeast-1", "Asia Pacific (Tokyo)"),
    ("ca-central-1", "Canada (Central)"),
    ("eu-central-1", "Europe (Frankfurt)"),
    ("eu-west-1", "Europe (Ireland)"),
    ("eu-west-2", "Europe (London)"),
    ("eu-south-1", "Europe (Milan)"),
    ("eu-west-3", "Europe (Paris)"),
    ("eu-north-1", "Europe (Stockholm)"),
    ("me-south-1", "Middle East (Bahrain)"),
    ("sa-east-1", "South America (São Paulo)"),
    ("us-gov-east-1", "AWS GovCloud (US-East)"),
    ("us-gov-west-1", "AWS GovCloud (US-West)")
    ]


class AccountRegisterForm(ModelForm):
    name = forms.CharField(
        label="Name",
        max_length=80,
        required=True,
    )

    account_number = forms.IntegerField(
        label="AWS Account Number",
        required=True,
    )

    region = forms.TypedChoiceField(
        label="AWS Region",
        required=True,
        widget=forms.Select,
        choices=AWS_REGION,
    )

    aws_access_key = forms.CharField(
        label="AWS Access Key",
        required=True,
    )

    aws_secret_key = forms.CharField(
        label="AWS Secret Key",
        required=True,
    )

    class Meta:
        model = AWS
        fields = ['name', 'account_number', 'region', 'aws_access_key', 'aws_secret_key']

