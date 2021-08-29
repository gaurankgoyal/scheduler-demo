from django.shortcuts import render, redirect
from .models import AWS
from django.contrib.auth.decorators import login_required
from .forms import AccountRegisterForm
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


def index(request):
    return render(request, 'scheduler/index.html')


@login_required
def home(request):
    context = {
        'accounts': AWS.objects.filter(owner=request.user)
    }
    return render(request, 'scheduler/home.html', context)


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
    return render(request, 'scheduler/add-account.html', {'form': form})


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
