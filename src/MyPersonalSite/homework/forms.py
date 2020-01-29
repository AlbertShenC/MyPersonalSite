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


class ReadingComprehensionQuestionPostForm(forms.ModelForm):
    class Meta:
        model = SingleChoiceQuestionPost
        fields = ('essay',
                  'stem_1', 'choice_1_1', 'choice_1_2', 'choice_1_3', 'choice_1_4', 'answer_1',
                  'stem_2', 'choice_2_1', 'choice_2_2', 'choice_2_3', 'choice_2_4', 'answer_2',
                  'stem_3', 'choice_3_1', 'choice_3_2', 'choice_3_3', 'choice_3_4', 'answer_3',
                  'stem_4', 'choice_4_1', 'choice_4_2', 'choice_4_3', 'choice_4_4', 'answer_4',
                  'stem_5', 'choice_5_1', 'choice_5_2', 'choice_5_3', 'choice_5_4', 'answer_5',
                  'stem_6', 'choice_6_1', 'choice_6_2', 'choice_6_3', 'choice_6_4', 'answer_6'
                  )
