from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import BlogPostForm
from .models import *
import markdown


def blog_list(request):
    if request.GET.get('order') == 'total_views':
        blog_list = BlogPost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        blog_list = BlogPost.objects.all()
        order = 'normal'
    paginator = Paginator(blog_list, 9)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    context = {'blogs': blogs, 'order': order}
    return render(request, 'blog/list.html', context)


def blog_main(request):
    return redirect('blog:blog_list')


def blog_detail(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    blog.total_views += 1
    blog.save(update_fields=['total_views'])
    blog.body = markdown.markdown(
        blog.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ]
    )
    context = {'blog': blog}
    return render(request, 'blog/detail.html', context)


@login_required(login_url='/user/login/')
def blog_create(request):
    if request.method == 'POST':
        blog_post_form = BlogPostForm(data=request.POST)
        if blog_post_form.is_valid():
            new_blog = blog_post_form.save(commit=False)
            new_blog.author = User.objects.get(id=request.user.id)
            new_blog.save()
            return redirect('blog:blog_list')
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        blog_post_form = BlogPostForm()
        context = {'blog_post_form': blog_post_form}
        return render(request, 'blog/create.html', context)


@login_required(login_url='/user/login/')
def blog_update(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)

    if request.user != blog.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method == 'POST':
        blog_post_form = BlogPostForm(data=request.POST)
        if blog_post_form.is_valid():
            blog.title = request.POST['title']
            blog.body = request.POST['body']
            blog.save()
            return redirect('blog:blog_detail', blog_id)
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        blog_post_form = BlogPostForm()
        context = {
            'blog': blog,
            'blog_post_form': blog_post_form}
        return render(request, 'blog/update.html', context)


@login_required(login_url='/user/login/')
def blog_delete(request, blog_id):
    if request.method == 'POST':
        blog = BlogPost.objects.get(id=blog_id)
        if request.user != blog.author:
            return HttpResponse("抱歉，你无权删除这篇文章。")
        blog.delete()
        return redirect('blog:blog_list')
    else:
        return HttpResponse("仅允许post请求")