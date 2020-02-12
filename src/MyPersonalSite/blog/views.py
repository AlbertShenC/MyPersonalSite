from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import BlogPostForm
from .models import *
from comment.models import Comment
from comment.forms import CommentForm
from MyPersonalSite.settings import MEDIA_ROOT
import markdown
import os, time
from PIL import Image


def blog_list(request):
    if request.method == 'GET':
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

        paginator = Paginator(blog_list, 9)
        page = request.GET.get('page')
        blogs = paginator.get_page(page)
        columns = BlogColumn.objects.all()
        context = {'blogs': blogs, 'order': order, 'search': search, 'column': column,
                   'tag': tag, 'columns': columns}
        return render(request, 'blog/list.html', context)
    else:
        context = {'error_message': '仅支持GET请求'}
        return render(request, 'error.html', context)


def blog_detail(request, blog_id):
    if request.method == 'GET':
        blog = BlogPost.objects.get(id=blog_id)
        comments = Comment.objects.filter(Blog=blog_id)
        blog.save(update_fields=['total_views'])
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        blog.body = md.convert(blog.body)
        comment_form = CommentForm()
        context = {'blog': blog, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form}
        return render(request, 'blog/detail.html', context)
    else:
        context = {'error_message': '仅支持GET请求'}
        return render(request, 'error.html', context)


def blog_first_view(request, blog_id):
    if request.method == 'POST':
        blog = BlogPost.objects.get(id=blog_id)
        blog.total_views += 1
        blog.save()
        return JsonResponse({
            'code': 'OK'
        })
    else:
        return JsonResponse({
            'code': 'ERROR',
            'message': '为安全起见，仅支持POST请求'
        })


def blog_like(request, blog_id):
    if request.method == 'POST':
        blog = BlogPost.objects.get(id=blog_id)
        blog.likes += 1
        blog.save()
        return JsonResponse({
            'code': 'OK'
        })
    else:
        return JsonResponse({
            'code': 'ERROR',
            'message': '为安全起见，仅支持POST请求'
        })


@login_required(login_url='/accounts/login/')
def blog_create(request):
    if not request.user.is_superuser:
        context = {'error_message': '抱歉，您无权发表文章，若有需求，请联系管理员'}
        return render(request, 'error.html', context)
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
            context = {'error_message': '表单内容有误，请重新填写'}
            return render(request, 'error.html', context)
    else:
        blog_post_form = BlogPostForm()
        columns = BlogColumn.objects.all()
        context = {'blog_post_form': blog_post_form, 'columns': columns}
        return render(request, 'blog/create.html', context)


@login_required(login_url='/accounts/login/')
def blog_update(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)

    if request.user != blog.author:
        context = {'error_message': '抱歉，你无权修改这篇文章。'}
        return render(request, 'error.html', context)

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
            context = {'error_message': '表单内容有误，请重新填写'}
            return render(request, 'error.html', context)
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


@login_required(login_url='/accounts/login/')
def blog_delete(request, blog_id):
    if request.method == 'POST':
        blog = BlogPost.objects.get(id=blog_id)
        if request.user != blog.author:
            context = {'error_message': '抱歉，你无权删除这篇文章。'}
            return render(request, 'error.html', context)
        blog.delete()
        return redirect('blog:blog_list')
    else:
        context = {'error_message': '为安全起见，仅允许POST请求'}
        return render(request, 'error.html', context)


@login_required(login_url='/accounts/login/')
def blog_add_picture(request):
    if not request.user.is_superuser:
        return HttpResponse('抱歉，您无权上传图片，若有需求，请联系管理员')

    if request.method == 'POST':
        img = request.FILES.get('img')
        time_path = time.strftime('%Y%m%d', time.localtime())
        blog_all_picture_path = os.path.join(MEDIA_ROOT + 'blog/', time_path)
        if not os.path.exists(blog_all_picture_path):
            os.mkdir(blog_all_picture_path)
        path = os.path.join(blog_all_picture_path, 'picture/')
        if not os.path.exists(path):
            os.mkdir(path)
        img_name = os.path.join(path, img.name)
        with open(img_name, 'wb') as ff:
            for c in img.chunks():
                ff.write(c)

        image = Image.open(img_name)
        (x, y) = image.size
        if x > 400:
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(img_name)

        img_url = '/media/blog/' + time_path + '/picture/' + img.name
        return HttpResponse("![](" + img_url + ")")
    elif request.method == 'GET':
        return render(request, 'blog/add_picture.html')
    else:
        return HttpResponse('仅支持GET和POST请求')
