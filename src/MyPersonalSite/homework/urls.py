# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'homework'

urlpatterns = [
    path('', views.homework_main, name='homework_main'),
    path('list/', views.homework_list, name='homework_list'),
    path('detail/<int:homework_id>/', views.homework_detail, name='homework_detail'),
    path('create/', views.homework_create, name='homework_create'),
    path('update/<int:homework_id>/', views.homework_update, name='homework_update'),
    path('delete/<int:homework_id>/', views.homework_delete, name='homework_delete'),
    path('submit_homework/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    # 查看某次作业某位学生成绩
    path('homework_grade/<int:homework_id>/<int:student_id>/', views.homework_grade, name='homework_grade'),
    # 批改某次作业某位学生作业
    path('mark_homework/<int:homework_id>/<int:student_id>/', views.mark_homework, name='mark_homework'),
    # 查看某班总览
    # path('class/<int:school_class_id>/', views.school_class, name='school_class'),
    # # 查看某班某次作业总览
    # path('class/<int:school_class_id>/homework/<int:homework_id>/', views.school_class_homework, name='school_class_homework'),
    # 查看某次作业总览
    path('homework_overview/<int:homework_id>/', views.homework_overview, name='homework_overview'),
    # 添加选择题
    path('create_choice_question/<int:homework_id>/', views.create_choice_question, name='create_choice_question'),

]