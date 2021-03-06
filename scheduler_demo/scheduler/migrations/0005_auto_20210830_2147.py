# Generated by Django 3.2.6 on 2021-08-30 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_alter_aws_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aws',
            name='name',
            field=models.CharField(help_text='Enter Account Name', max_length=30),
        ),
        migrations.CreateModel(
            name='CronJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a Cron Job Name', max_length=30)),
                ('start_cronjob', models.CharField(help_text="Enter Cron Job for the scheduler eg '* * * ? * *'", max_length=30)),
                ('stop_cronjob', models.CharField(help_text="Enter Cron Job for the scheduler eg '* * * ? * *'", max_length=30)),
                ('instance_id', models.CharField(help_text='Instance Id', max_length=30)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.aws')),
            ],
        ),
    ]
