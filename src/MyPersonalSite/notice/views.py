from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required(login_url='/user/login/')
def comment_notice_list(request):
    notices_unread = request.user.notifications.unread()
    notices_read = request.user.notifications.read()
    context = {
        'notices_unread': notices_unread,
        'notices_read': notices_read
    }
    return render(request, 'notice/list.html', context)


@login_required(login_url='/user/login/')
def comment_notice_update(request):
    notice_id = request.GET.get('notice_id')
    if notice_id:
        blog_id = request.GET.get('blog_id')
        request.user.notifications.get(id=notice_id).mark_as_read()
        return redirect(reverse('blog:blog_detail', args=[blog_id]))
    else:
        request.user.notifications.mark_all_as_read()
        return redirect('notice:comment_notice_list')

