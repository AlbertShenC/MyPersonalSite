# Author    :Albert Shen
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import JsonResponse
import time


def main_page(request):
    return redirect('blog:blog_main')


def get_time(request):
    return JsonResponse({
        "time": int(time.time())
    })