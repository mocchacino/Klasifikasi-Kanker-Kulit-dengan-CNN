from django.contrib import admin
from django.urls import path, include
from static_page import views

urlpatterns = [
    path('', views.homepage, name='homepage')
]