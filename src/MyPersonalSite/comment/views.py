from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from notifications.signals import notify
from django.contrib.auth.models import User

from blog.models import BlogPost
from .forms import CommentForm
from .models import Comment

# Create your views here.

@login_required(login_url='/user/login/')
def post_comment(request, blog_id, parent_comment_id=None):
    blog = get_object_or_404(BlogPost, id=blog_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.Blog = blog
            new_comment.user = request.user

            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                if not parent_comment.user == new_comment.user:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你：' + new_comment.body[0:10] + '...',
                        target=blog,
                        action_object=new_comment,
                    )
                return HttpResponse('200 OK')

            new_comment.save()
            if not blog.author == new_comment.user:
                notify.send(
                    request.user,
                    recipient=blog.author,
                    verb='回复了你：' + new_comment.body[0:10] + '...',
                    target=blog,
                    action_object=new_comment,
                )
            return redirect(reverse('blog:blog_detail', args=[blog_id]))
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'blog_id': blog_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse("仅接受GET/POST请求。")