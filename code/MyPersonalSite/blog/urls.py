# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('list/', views.blog_list, name='blog_list'),
    path('detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('delete/<int:blog_id>/', views.blog_delete, name='blog_delete'),
]