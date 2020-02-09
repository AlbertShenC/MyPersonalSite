from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required


def login_validate(request):
    if request.method == 'POST':
        id_login = request.POST.get('id_login')
        id_password = request.POST.get('id_password')
        # 使用用户名登陆
        if id_login.find('@') == -1:
            user = User.objects.filter(username=id_login)
        # 使用邮箱登陆
        else:
            user = User.objects.filter(email=id_login)
        # 验证密码
        if len(user) == 1 and user[0].check_password(id_password):
            return JsonResponse({
                'code': 'OK'
            })
        else:
            return JsonResponse({
                'code': 'ERROR',
                'message': '账号或密码错误'
            })
    else:
        return JsonResponse({
            'code': 'ERROR',
            'message': '为安全起见，仅支持POST请求'
        })


def signup_validate(request):
    if request.method == 'POST':
        id_username = request.POST.get('id_username')
        id_email = request.POST.get('id_email')
        id_password1 = request.POST.get('id_password1')
        id_password2 = request.POST.get('id_password2')
        if not id_username.isalnum():
            return JsonResponse({
                'code': 'ERROR',
                'message': '用户名仅能使用字母及数字'
            })
        if id_email.find('@') == -1:
            return JsonResponse({
                'code': 'ERROR',
                'message': '邮箱格式错误'
            })
        if id_password1 != id_password2:
            return JsonResponse({
                'code': 'ERROR',
                'message': '两次输入的密码不相同'
            })
        if len(User.objects.filter(username=id_username)) != 0:
            return JsonResponse({
                'code': 'ERROR',
                'message': '用户名已存在'
            })
        if len(User.objects.filter(email=id_email)) != 0:
            return JsonResponse({
                'code': 'ERROR',
                'message': '邮箱已存在'
            })
        return JsonResponse({
            'code': 'OK'
        })
    else:
        return JsonResponse({
            'code': 'ERROR',
            'message': '为安全起见，仅支持POST请求'
        })


@login_required(login_url='/accounts/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        if request.user != user:
            context = {'error_message': '抱歉，你没有权限修改此用户信息。'}
            return render(request, 'error.html', context)
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd.get('phone')
            profile.bio = profile_cd.get('bio')
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd.get('avatar')
            profile.save()
            return redirect('user:profile_edit', id=id)
        else:
            context = {'error_message': '抱歉，输入有误，请重新输入。'}
            return render(request, 'error.html', context)
    else:
        profile_form = ProfileForm()
        context = {'profile_form': profile_form,
                   'profile': profile,
                   'user': user}
        return render(request, 'user/edit.html', context)

