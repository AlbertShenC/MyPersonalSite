# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'homework'

urlpatterns = [
    path('', views.homework_main, name='homework_main'),
    # 作业列表
    path('list/', views.homework_list, name='homework_list'),
    # 作业详情
    path('detail/<int:homework_id>/', views.homework_detail, name='homework_detail'),
    # 新建作业
    path('create/', views.homework_create, name='homework_create'),
    # 更新作业
    path('update/<int:homework_id>/', views.homework_update, name='homework_update'),
    # 删除作业
    path('delete/<int:homework_id>/', views.homework_delete, name='homework_delete'),
    # 学生提交作业
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

    # 删除大题
    path('delete_big_question/<int:big_question_id>/', views.delete_big_question, name='delete_big_question'),
    # 删除小题
    path('delete_small_question/<int:small_question_id>/', views.delete_small_question, name='delete_small_question'),


    # 添加选择题
    path('create_choice_question/<int:homework_id>/', views.create_choice_question, name='create_choice_question'),
    # 修改选择题
    path('update_choice_question/<int:big_question_id>/', views.update_choice_question, name='update_choice_question'),

    # 添加阅读理解大题
    path('create_reading_comprehension_question/<int:homework_id>/', views.create_reading_comprehension_question,
         name='create_reading_comprehension_question'),

    # 添加完形填空大题
    path('create_cloze_question/<int:homework_id>/', views.create_cloze_question,
         name='create_cloze_question'),

    # 修改大题
    path('update_big_question/<int:big_question_id>/', views.update_big_question,
         name='update_big_question'),
    # 修改小题
    path('update_small_question/<int:question_id>/', views.update_small_question,
         name='update_small_question'),
]