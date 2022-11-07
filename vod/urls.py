from django.urls import path, include
from vod import views

urlpatterns = [
    path('', views.Home, name='home'),
]
