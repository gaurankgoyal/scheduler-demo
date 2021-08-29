from django.urls import path
from .views import AccountListView, AccountCreateView, AccountUpdateView, AccountDeleteView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='scheduler-home'),
    path('aws_account/<str:account_number>/details', views.select_account, name='account-details'),
    path('aws_account/<str:account_number>/<str:instance_id>/start', views.start_ec2, name='start-ec2'),
    path('aws_account/<str:account_number>/<str:instance_id>/stop', views.stop_ec2, name='stop-ec2'),
    path('about/', views.about, name='scheduler-about'),
    path('account/new/', AccountCreateView.as_view(), name='add-account'),
    path('account/<int:pk>/update/', AccountUpdateView.as_view(), name='update-account'),
    path('account/<int:pk>/delete/', AccountDeleteView.as_view(), name='delete-account'),
    path('accounts/', AccountListView.as_view(), name='accounts'),
]
