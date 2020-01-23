# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('post_comment/<int:blog_id>/', views.post_comment, name='post_comment'),
]