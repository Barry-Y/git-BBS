"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.views.static import serve
from BBS import settings
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', views.home,name='home'),
    url(r'^register/', views.register,name='register'),
    url(r'^login/', views.login,name='login'),
    url(r'^logout/', views.logout,name='logout'),
    url(r'^set_password/', views.set_password,name='set_password'),
    #图片验证码相关操作
    url(r'^get_code/', views.get_code),
    #点赞点踩
    url(r'^up_or_down/',views.up_or_down),
    #评论
    url(r'^comment/',views.comment),

    #暴露后端指定文件夹资源
    #在暴露资源的时候一定要明确该资源是否可以暴露
    url(r'^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),

    #后台管理
    url(r'^backend/',views.backend,name='backend'),
    #添加文章
    url(r'^add/article/',views.add_article,name='add_article'),
    #编辑器上传图片
    url(r'^upload_image/',views.upload_image),
    #修改用户头像
    url(r'^set/avatar',views.set_avatar,name='set_avatar'),

    #个人站点页面搭建
    url(r'^(?P<username>\w+)/$',views.site),
    #侧边栏的筛选功能(基于个人站点)
    # url(r'^(?P<username>\w+)/tag/(\d+)/',views.site),
    # url(r'^(?P<username>\w+)/category/(\d+)/',views.site),
    # url(r'^(?P<username>\w+)/archive/(\w+)/',views.site),
    #合并url，后端接收的参数要设置成万能关键字参数**kwargs(多个url指向同一个视图函数)
    url(r'^(?P<username>\w+)/(?P<condition>tag|category|archives)/(?P<param>.*)',views.site),
    #文章详情页
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)',views.article_detail),
    url(r'^favicon.ico',RedirectView.as_view(url='static/img/favicon.ico')),
]
