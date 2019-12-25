# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()