from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='scheduler-home'),
    path('about', views.about, name='scheduler-about'),
    path('add', views.about, name='add-account'),
]
