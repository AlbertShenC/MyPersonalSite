# Author    :Albert Shen
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password_confirm = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password_confirm(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password_confirm'):
            return data.get('password')
        else:
            raise forms.ValidationError('两次密码输入不一致。')


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()