# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django import forms
from .models import *


class HomeworkPostForm(forms.ModelForm):
    class Meta:
        model = HomeworkPost
        fields = ('title', 'instrument')


class SingleChoiceQuestionPostForm(forms.ModelForm):
    class Meta:
        model = SingleChoiceQuestionPost
        fields = ('stem', 'choice_1', 'choice_2', 'choice_3', 'choice_4', 'answer')
