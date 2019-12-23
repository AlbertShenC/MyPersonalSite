from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BlogPostForm
from django.contrib.auth.models import User
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

def blog_create(request):
    if request.method == 'POST':
        blog_post_form = BlogPostForm(data = request.POST)
        if blog_post_form.is_valid():
            new_blog = blog_post_form.save(commit = False)
            new_blog.author = User.objects.get(id = 1)
            new_blog.save()
            return redirect('blog:blog_list')
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        blog_post_form = BlogPostForm()
        context = {'blog_post_form': blog_post_form}
        return render(request, 'blog/create.html', context)

