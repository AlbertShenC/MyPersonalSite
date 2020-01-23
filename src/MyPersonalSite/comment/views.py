from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse

from blog.models import BlogPost
from .forms import CommentForm

# Create your views here.

@login_required(login_url='/user/login/')
def post_comment(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.Blog = blog
            new_comment.user = request.user
            new_comment.save()
            return redirect(reverse('blog:blog_detail', args=[blog_id]))
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        return HttpResponse("发表评论仅接受POST请求。")