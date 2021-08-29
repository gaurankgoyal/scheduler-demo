from django.urls import path
from .views import AccountListView, AccountCreateView, AccountUpdateView, AccountDeleteView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='scheduler-home'),
    path('about/', views.about, name='scheduler-about'),
    path('account/new/', AccountCreateView.as_view(), name='add-account'),
    path('account/<int:pk>/update', AccountUpdateView.as_view(), name='update-account'),
    path('account/<int:pk>/delete', AccountDeleteView.as_view(), name='delete-account'),
    path('accounts/', AccountListView.as_view(), name='accounts'),
]
