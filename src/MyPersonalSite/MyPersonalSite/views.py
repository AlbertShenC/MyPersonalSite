# Author    :Albert Shen
# -*- coding: utf-8 -*-
from django.shortcuts import redirect


def main_page(request):
    return redirect('blog:blog_main')