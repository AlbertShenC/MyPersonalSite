from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import BlogPostForm
from .models import *
from comment.models import Comment
import markdown


def blog_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    blog_list = BlogPost.objects.all()

    if search:
        blog_list = blog_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    if column is not None and column.isdigit():
        blog_list = blog_list.filter(column=column)

    if tag and tag != 'None':
        blog_list = blog_list.filter(tags__name__in=[tag])

    if order == 'total_views':
        blog_list = blog_list.order_by('-total_views')

    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    context = {
        'blogs': blogs,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }

    return render(request, 'blog/list.html', context)


def blog_main(request):
    return redirect('blog:blog_list')


def blog_detail(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    comments = Comment.objects.filter(Blog=blog_id)
    blog.total_views += 1
    blog.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    blog.body = md.convert(blog.body)
    context = {'blog': blog, 'toc': md.toc, 'comments': comments}
    return render(request, 'blog/detail.html', context)


@login_required(login_url='/user/login/')
def blog_create(request):
    if request.method == 'POST':
        blog_post_form = BlogPostForm(request.POST, request.FILES)
        if blog_post_form.is_valid():
            new_blog = blog_post_form.save(commit=False)
            new_blog.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_blog.column = BlogColumn.objects.get(id=request.POST['column'])
            new_blog.save()
            blog_post_form.save_m2m()
            return redirect('blog:blog_list')
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        blog_post_form = BlogPostForm()
        columns = BlogColumn.objects.all()
        context = {'blog_post_form': blog_post_form, 'columns': columns}
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
            if request.POST['column'] != 'none':
                blog.column = BlogColumn.objects.get(id=request.POST['column'])
            else:
                blog.column = None

            if request.FILES.get('avatar'):
                blog.avatar = request.FILES.get('avatar')

            blog.tags.set(*request.POST.get('tags').split(','), clear=True)
            blog.save()
            return redirect('blog:blog_detail', blog_id)
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        blog_post_form = BlogPostForm()
        columns = BlogColumn.objects.all()
        context = {
            'blog': blog,
            'blog_post_form': blog_post_form,
            'columns': columns,
            'tags': ','.join([x for x in blog.tags.names()]),
        }
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