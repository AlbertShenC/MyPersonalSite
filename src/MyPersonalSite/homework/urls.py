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
    path('create_single_choice_question/<int:homework_id>/', views.create_single_choice_question,
         name='create_single_choice_question'),
    path('update_single_choice_question/<int:question_id>/', views.update_single_choice_question,
         name='update_single_choice_question'),
    path('delete_single_choice_question/<int:question_id>/', views.delete_single_choice_question,
         name='delete_single_choice_question'),
    path('create_reading_comprehension_question/<int:homework_id>/', views.create_reading_comprehension_question,
         name='create_reading_comprehension_question'),
    path('update_reading_comprehension_question/<int:question_id>/', views.update_reading_comprehension_question,
         name='update_reading_comprehension_question'),
    path('delete_reading_comprehension_question/<int:question_id>/', views.delete_reading_comprehension_question,
         name='delete_reading_comprehension_question'),
]