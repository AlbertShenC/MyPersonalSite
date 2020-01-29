# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'intro'

urlpatterns = [
    path('', views.intro_main, name='intro_main'),
]