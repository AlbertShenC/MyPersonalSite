from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data.get('password'))
            new_user.save()
            login(request, new_user)
            return redirect('blog:blog_list')
        else:
            return HttpResponse('注册信息错误。')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'user_register_form': user_register_form}
        return render(request, 'user/register.html', context)
    else:
        return HttpResponse('请求类型不是Post或Get。')


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                return redirect('blog:blog_list')
            else:
                return HttpResponse('账号或密码错误。')
        else:
            return HttpResponse('账号或密码错误')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'user_login_form': user_login_form}
        return render(request, 'user/login.html', context)
    else:
        return HttpResponse('请求类型不是Post或Get。')


def user_logout(request):
    logout(request)
    return redirect('blog:blog_list')


@login_required(login_url='user/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('blog:blog_list')
        else:
            return HttpResponse('你没有删除用户的权限。')
    else:
        return HttpResponse('请求类型不是Post。')


@login_required(login_url='/user/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse('你没有权限修改此用户信息')
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd.get('phone')
            profile.bio = profile_cd.get('bio')
            profile.examination_number = profile_cd.get('examination_number')
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd.get('avatar')
            profile.save()
            return redirect('user:profile_edit', id=id)
        else:
            return HttpResponse('输入有误，请重新输入')
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form,
                   'profile': profile,
                   'user': user}
        return render(request, 'user/edit.html', context)
    else:
        return HttpResponse('请求类型不是Post或Get。')


# 教师添加修改班级
@login_required(login_url='/user/login/')
def update_school_class(request):
    if request.method == 'POST':
        return
    elif request.method == 'GET':
        return
    else:
        return 