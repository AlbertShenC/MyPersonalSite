from django.shortcuts import render
from django.http import HttpResponse

from .models import *
import markdown


def blog_list(request):
    blogs = BlogPost.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blog/list.html', context)


def blog_detail(request, id):
    blog = BlogPost.objects.get(id = id)
    blog.body = markdown.markdown(
        blog.body,
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ]
    )
    context = {'blog': blog}
    return render(request, 'blog/detail.html', context)

