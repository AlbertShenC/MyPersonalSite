# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('logout/', views.user_logout, name='user_logout'),
    path('delete/<int:id>', views.user_delete, name='user_delete'),
    path('edit/<int:id>', views.profile_edit, name='profile_edit'),
]