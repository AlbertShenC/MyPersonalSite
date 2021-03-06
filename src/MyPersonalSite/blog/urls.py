# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_main'),
    path('list/', views.blog_list, name='blog_list'),
    path('detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('delete/<int:blog_id>/', views.blog_delete, name='blog_delete'),
    path('update/<int:blog_id>/', views.blog_update, name='blog_update'),
    path('like/<int:blog_id>/', views.blog_like, name='blog_like'),
    path('first_view/<int:blog_id>/', views.blog_first_view, name='blog_first_view'),
    path('blog_add_picture/', views.blog_add_picture, name='blog_add_picture'),
]