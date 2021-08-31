from django.shortcuts import render, redirect
from .models import AWS, CronJob
from django.contrib.auth.decorators import login_required
from .forms import AccountRegisterForm, SchedulerCreationForm
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .utils import (get_ec2_instance,
                    start_instance,
                    stop_instance,
                    get_rds_instance,
                    stop_rds_instance,
                    start_rds_instance,
                    create_start_cron_job,
                    create_stop_cron_job,
                    aws_delete_schedule)
from botocore.exceptions import ClientError


def index(request):
    return render(request, 'scheduler/index.html')


@login_required
def home(request):
    context = {
        'accounts': AWS.objects.filter(owner=request.user)
    }
    return render(request, 'scheduler/home.html', context)


@login_required
def select_account(request, account_number):
    aws = AWS.objects.all().filter(account_number=account_number, owner=request.user).first()
    try:
        ec2_list = get_ec2_instance(aws.region, aws.aws_access_key, aws.aws_secret_key, aws)
        rds_list = get_rds_instance(aws.region, aws.aws_access_key, aws.aws_secret_key, aws)
    except ClientError as e:
        messages.warning(request, str(e))
        context = {
            'accounts': AWS.objects.all().filter(owner=request.user),
        }
        return render(request, 'scheduler/account_details.html', context)
    if len(ec2_list) == 0 and len(rds_list) == 0:
        messages.warning(request, f'No EC2 Instance or RDS found on AWS Account - {account_number}!')
    context = {
        'accounts': AWS.objects.all().filter(owner=request.user),
        'ec2_details': ec2_list,
        'aws_account': AWS.objects.all().filter(account_number=account_number, owner=request.user),
        'rds_details': rds_list
    }
    return render(request, 'scheduler/account_details.html', context)


@login_required
def start_ec2(request, account_number, instance_id):
    aws = AWS.objects.all().filter(account_number=account_number, owner=request.user).first()
    start_instance(aws.region, aws.aws_access_key, aws.aws_secret_key, instance_id)
    messages.success(request, f'Instance-{instance_id} in Account-{account_number} has been started !')
    return redirect('account-details', account_number)


@login_required
def stop_ec2(request, account_number, instance_id):
    aws = AWS.objects.all().filter(account_number=account_number, owner=request.user).first()
    stop_instance(aws.region, aws.aws_access_key, aws.aws_secret_key, instance_id)
    messages.success(request, f'Instance-{instance_id} in Account-{account_number} has been Stopped !')
    return redirect('account-details', account_number)


@login_required
def start_rds(request, account_number, rds_identifier):
    aws = AWS.objects.all().filter(account_number=account_number, owner=request.user).first()
    message = start_rds_instance(aws.region, aws.aws_access_key, aws.aws_secret_key, rds_identifier)
    if "successfully" in message:
        messages.success(request, message)
    else:
        messages.warning(request, message)
    return redirect('account-details', account_number)


@login_required
def stop_rds(request, account_number, rds_identifier):
    aws = AWS.objects.all().filter(account_number=account_number, owner=request.user).first()
    message = stop_rds_instance(aws.region, aws.aws_access_key, aws.aws_secret_key, rds_identifier)
    if "successfully" in message:
        messages.success(request, message)
    else:
        messages.warning(request, message)
    return redirect('account-details', account_number)


@login_required
def about(request):
    context = {
        'accounts': AWS.objects.filter(owner=request.user)
    }
    return render(request, 'scheduler/about.html', context)


@login_required
def add_account(request):
    if request.method == "POST":
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account Has Been Added')
            return redirect('scheduler-home')
    form = AccountRegisterForm()
    context = {
        'accounts': AWS.objects.filter(owner=request.user),
        'form': form
    }
    return render(request, 'scheduler/add-account.html', context)


@login_required
def scheduler(request, account_number, instance_id):
    aws = AWS.objects.all().filter(account_number=account_number, owner=request.user).first()
    cronjob = CronJob.objects.all().filter(instance_id=instance_id).first()
    update = True
    if request.method == "POST":
        form = SchedulerCreationForm(request.POST)
        if form.is_valid():
            create_start_cron_job(
                aws.region,
                aws.aws_access_key,
                aws.aws_secret_key,
                instance_id,
                form.cleaned_data['start_cronjob'],
                str(request.user))
            message = create_stop_cron_job(
                aws.region,
                aws.aws_access_key,
                aws.aws_secret_key,
                instance_id,
                form.cleaned_data['stop_cronjob'],
                str(request.user))
            CronJob.objects.update_or_create(
                aws_name_start=form.cleaned_data['aws_name_start'],
                aws_name_stop=form.cleaned_data['aws_name_stop'],
                instance_id=form.cleaned_data['instance_id'],
                defaults={
                    "name": form.cleaned_data['name'],
                    "account": form.cleaned_data['account'],
                    "start_cronjob": form.cleaned_data['start_cronjob'],
                    "stop_cronjob": form.cleaned_data['stop_cronjob']
                }
            )
            messages.success(request, message)
            return redirect('account-details', account_number)
    if CronJob.objects.all().filter(instance_id=instance_id).exists():
        form = SchedulerCreationForm(initial={'name': cronjob.name,
                                              'start_cronjob': cronjob.start_cronjob,
                                              'stop_cronjob': cronjob.stop_cronjob})
    else:
        form = SchedulerCreationForm()
        update = False
    context = {
        'form': form,
        'instance_id': instance_id,
        'account': aws,
        'accounts': AWS.objects.filter(owner=request.user),
        'update': update
    }
    return render(request, 'scheduler/scheduler.html', context)


@login_required
def delete_schedule(request, aws_name_start, account_number):
    aws = AWS.objects.all().filter(account_number=account_number, owner=request.user).first()
    if aws_delete_schedule(aws.region,
                           aws.aws_access_key,
                           aws.aws_secret_key,
                           aws_name_start):
        CronJob.objects.all().filter(aws_name_start=aws_name_start).delete()
        messages.info(request, "Cron Schedule was removed")

    else:
        messages.warning(request, "Error while deleting the schedule")
    return redirect('account-details', account_number)


class AccountListView(LoginRequiredMixin, ListView):
    model = AWS
    template_name = 'scheduler/accounts.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return AWS.objects.filter(owner=self.request.user)


class AccountCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AWS
    template_name = 'scheduler/add-account.html'
    fields = ['name', 'account_number', 'region', 'aws_access_key', 'aws_secret_key']
    success_message = "AWS Account was Successfully Added!!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = AWS
    template_name = 'scheduler/aws_update.html'
    fields = ['name', 'account_number', 'region', 'aws_access_key', 'aws_secret_key']
    success_message = "AWS Account was Successfully Updated!!"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        aws = self.get_object()
        if self.request.user == aws.owner:
            return True
        return False


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = AWS
    success_url = '/accounts'
    success_message = "AWS Account was Removed!!"

    def test_func(self):
        aws = self.get_object()
        if self.request.user == aws.owner:
            return True
        return False

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
