# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    # 通知列表
    path('list/', views.comment_notice_list, name='comment_notice_list'),
    # 更新通知状态
    path('update/', views.comment_notice_update, name='comment_notice_update'),
]