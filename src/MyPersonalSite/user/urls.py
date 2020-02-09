# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login_validate/', views.login_validate, name='login_validate'),
    path('signup_validate/', views.signup_validate, name='signup_validate'),
    path('edit/<int:id>', views.profile_edit, name='profile_edit'),
]