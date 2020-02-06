"""MyPersonalSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls
from blog.views import blog_list

urlpatterns = [
    path('admin/', admin.site.urls),

    # 个人简历
    path('intro/', include('intro.urls', namespace='intro')),

    # 首页
    path('', blog_list, name='home'),

    # 用户
    path('user/', include('user.urls', namespace='user')),

    # 博客
    path('blog/', include('blog.urls', namespace='blog')),

    # 密码重置
    path('password_reset/', include('password_reset.urls')),

    # 评论
    path('comment/', include('comment.urls', namespace='comment')),

    # 通知（norifications库自带）
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),

    # 通知
    path('notice/', include('notice.urls', namespace='notice')),

    # 第三方登陆
    path('accounts/', include('allauth.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)