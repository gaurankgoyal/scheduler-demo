# Generated by Django 3.2.6 on 2021-08-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aws',
            name='account_number',
            field=models.CharField(help_text='Enter AWS Account Number', max_length=12),
        ),
    ]
