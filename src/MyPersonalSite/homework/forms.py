# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django import forms
from .models import *


class HomeworkPostForm(forms.ModelForm):
    class Meta:
        model = HomeworkPost
        fields = ('title', 'instrument')
