from django.shortcuts import render,HttpResponse,redirect
from app01.myforms.regform import MyRegForm
from app01 import models
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count,F
from django.db.models.functions import TruncMonth
import json
import os
from BBS import settings

# Create your views here.
def home(request):
    #查询本网站所有的文章数据展示的前端页面（这里可以使用分页器做分页）
    article_queryset = models.Article.objects.all()
    return render(request,'home.html',locals())


def register(request):
    form_obj = MyRegForm()
    if request.method == 'POST':
        # 返回给前端校验结果
        back_dict = {'code': 1000, 'msg': ''}
        # 校验ajax提交的数据是否合法
        form_obj = MyRegForm(request.POST)
        if form_obj.is_valid():
            #删除一个确认密码字段
            clean_data = form_obj.cleaned_data
            clean_data.pop('confirm_password') #clean_data = {'username':'Barry','password':'Barry123','email':'123@qq.com'}
            #用户头像(判断是否传头像)
            file_obj = request.FILES.get('avatar')
            if file_obj:
                #如果有头像，把默认头像修改为新的头像
                clean_data['avatar'] = file_obj
            #操作数据库保存数据
            models.UserInfo.objects.create_user(**clean_data)#字典打散()
            #注册成功后给前端增加一个登陆url
            back_dict['url'] = '/login/'
        else:
            back_dict['code'] = 2000
            back_dict['msg'] = form_obj.errors
        return JsonResponse(back_dict)
    return render(request,'register.html',locals())


def login(request):
    if request.method == 'POST':
        back_dict = {'code':1000,'msg':''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        #先校验验证码是否正确(忽略大小写)
        if request.session.get('code').upper() == code.upper():
            #校验用户名和密码是否正确(用auth模块)
            user_obj = auth.authenticate(request,username=username,password=password)
            if user_obj:
                #保存用户状态
                auth.login(request,user_obj)
                back_dict['url'] = '/home/'
            else:
                back_dict['code'] = 1001
                back_dict['msg'] = '用户名或密码错误'
        else:
            back_dict['code'] = 1002
            back_dict['msg'] = '验证码错误'
        return JsonResponse(back_dict)
    return render(request,'login.html',locals())


def logout(request):
    auth.logout(request)
    return redirect('/home/')


def set_password(request):
    if request.is_ajax():
        back_dict = {'code': 1000, 'msg': ''}
        if request.method == 'POST':
            confirm_password = request.POST.get('confirm_password')
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            is_right = request.user.check_password(old_password)
            if is_right:
                if 3 <= len(new_password) <= 8:
                    if new_password == confirm_password:
                        request.user.set_password(new_password)
                        request.user.save()
                        back_dict['url'] = '/home/'
                    else :
                        back_dict['code'] = 1001
                        back_dict['msg'] = '两次密码不一致'
                else:
                    back_dict['code'] = 1002
                    back_dict['msg'] = '请输入3～8位密码'
            else:
                back_dict['code'] = 1003
                back_dict['msg'] = '原密码错误'
        return JsonResponse(back_dict)



'''
图片相关模块
    pip3 install pillow
Image:生成图片
ImageDraw:能够在图片上乱涂乱画
ImageFont:控制字体样式
'''
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO,StringIO
'''
内存管理模块
BytesIO:临时帮你存储数据 返回的时候数据是二进制
StringIO:临时帮你存储数据 返回的时候数据是字符串
'''
import random

def get_random():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)


def get_code(request):
    # return HttpResponse('666')
    #利用pillow模块动态产生图片
    img_obj = Image.new('RGB',(200,35),get_random())
    #创建一个画笔对象
    img_draw = ImageDraw.Draw(img_obj)
    #字体样式、大小
    img_font = ImageFont.truetype('app01/static/font/222.ttf',30)
    #随机验证码：五位、数字、大小写字母
    code = ''
    for i in range(5):
        random_upper = chr(random.randint(65,90))#大写字母
        random_lower = chr(random.randint(97,122))#小写字母
        random_int = str(random.randint(0,9))#数字
        #随机选择一个
        tmp = random.choice([random_upper,random_lower,random_int])
        #将产生的随机字符串写入到图片上
        img_draw.text((i*45,0),tmp,get_random(),img_font)
        '''
        一个个写入图片上可以控制每个字体的间隙
        '''
        #拼接随机字符串
        code += tmp
    print(code)
    #随机验证码在登陆的视图函数里需要用到，要比对，所以需要存起来让其他视图函数可以使用到
    request.session['code'] = code
    # 先创建一个内存管理对象，类似句柄f
    io_obj = BytesIO()
    img_obj.save(io_obj,'png')
    # 从内存管理器中读取二进制的图片返回给前端
    return HttpResponse(io_obj.getvalue())


def site(request,username,**kwargs):
    '''

    :param request:
    :param username:
    :param kwargs: 如果该参数有值，需要对article_list做额外的筛选
    :return:
    '''
    #先校验当前用户名对应的个人站点是否存在
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return render(request,'errors.html')
    blog = user_obj.blog
    # 查询当前个人站点下的所有的文章
    article_list = models.Article.objects.filter(blog=blog)
    if kwargs:
        #print(kwargs) {'condition': 'tag', 'param': '1'}
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        #判断用户向按照哪个条件筛选数据(标签/分类/日期归档)
        if condition == 'tag':
            article_list = article_list.filter(tags__pk=param)#多对多跨表查询
        elif condition == 'category':
            article_list = article_list.filter(category_id=param)
        else:
            year,month = param.split('-') #2021-12 [2021,1]
            article_list = article_list.filter(create_time__year=year,create_time__month=month)
    # 查询当前用户所有的分类及分类下的文章数
    # category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list('name','count_num','pk')
    # #print(category_list)<QuerySet [('Barry的分类一', 2), ('Barry的分类二', 1), ('Barry的分类三', 1)]>
    # # 查询当前用户所有的标签及标签下的文章数
    # tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list('name','count_num','pk')
    # # 按年月统计当前用户的所有的文章
    # date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values('month').annotate(count_num=Count('pk')).values_list('month','count_num')
    # # print(date_list)
    return render(request,'site.html',locals())


def article_detail(request,username,article_id):
    '''
    需要校验username和article_id是否存在
    :param request:
    :param username:
    :param article_id:
    :return:
    '''
    #继承的模板中需要blog
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    #先获取文章对象(必须限定文章的对象)
    article_obj = models.Article.objects.filter(pk=article_id,blog__userinfo__username=username).first()
    if not article_obj:
        return render(request, 'errors.html')
    #获取当前文章的所有评论内容的对象
    comment_list = models.Comment.objects.filter(article_id=article_id)
    return render(request,'article_detail.html',locals())


def up_or_down(request):
    '''
    1.登陆用户才可以点赞
    2.自己不能给自己点赞
    3.不能重复点赞或点踩
    4.操作数据库
    :param request:
    :return:
    '''
    if request.is_ajax():
        back_dict = {'code':1000,'msg':''}
        #先判断当前用户是否登陆
        is_login = request.user.is_authenticated()
        if is_login:
            article_id = request.POST.get('article_id')
            # 注意这个is_up是json格式的字符串
            is_up = request.POST.get('is_up')
            is_up = json.loads(is_up)
            # print(is_up,type(is_up))True <class 'bool'>
            #判断当前文章的用户是否自己
            #根据文章id查询文章对象，根据文章对象查作者
            article_obj = models.Article.objects.filter(pk=article_id).first()
            #文章的作者对象不等于当前登陆的对象
            if not article_obj.blog.userinfo == request.user:
                #校验当前用户是否已点赞或点踩
                is_click = models.UpAndDown.objects.filter(user=request.user,article=article_obj)
                if not is_click:
                    #操作数据库(要同步操作普通字段)
                    #判断当前用户是点赞还是点踩
                    if is_up:
                        #给点赞数加1
                        models.Article.objects.filter(pk=article_id).update(up_num=F('up_num')+1)
                        back_dict['msg'] = '点赞成功!'
                    else:
                        models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                        back_dict['msg'] = '点踩成功!'
                    #操作点赞点踩表
                    models.UpAndDown.objects.create(user=request.user,article=article_obj,is_up=is_up)
                else:
                    back_dict['code'] = 1001
                    back_dict['msg'] = '您已支持过!'
            else:
                if is_up:
                    back_dict['code'] = 1002
                    back_dict['msg'] = '您不能给自己点赞!'
                else:
                    back_dict['code'] = 1003
                    back_dict['msg'] = '您不能给自己点踩!'
        else:
            back_dict['code'] = 1004
            back_dict['msg'] = '请先<a href="/login/">登陆</a>'
        return JsonResponse(back_dict)


def comment(request):
    if request.is_ajax():
        back_dict = {'code': 1000, 'msg': ''}
        if request.method == 'POST':
            if request.user.is_authenticated():
                article_id = request.POST.get('article_id')
                content = request.POST.get('content')
                parent_id = request.POST.get('parent_id')
                #操作数据库存储数据(评论表中的内容、文章表中的评论数)
                #修改数据
                models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num')+1)
                #添加数据
                models.Comment.objects.create(user=request.user,article_id=article_id,content=content,parent_id=parent_id)
                back_dict['msg'] = '感谢您的评论！'
            else:
                back_dict['code'] = 1001
                back_dict['msg'] = '请先<a herf="/login/">登陆</a>再评论'
            return JsonResponse(back_dict)


#导入分页器
from utils.mypage import Pagination
@login_required
def backend(request):
    article_list = models.Article.objects.filter(blog=request.user.blog)
    page_obj = Pagination(current_page=request.GET.get('page',1),all_count=article_list.count())
    page_queryset = article_list[page_obj.start:page_obj.end]
    return render(request, 'backend/backend.html',locals())


from bs4 import BeautifulSoup
@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        #标签是多选的，可以有多个值
        tag_id_list = request.POST.getlist('tag')
        #使用BeautifulSoup模块
        soup = BeautifulSoup(content,'html.parser')
        #获取所有的标签
        tags = soup.find_all()
        for tag in tags:
            # print(tag.name) 获取页面所有的标签名
            # 删除script标签(避免xss攻击)
            if tag.name == 'script':
                tag.decompose()
        #文章简介(截取文本150个)
        desc = soup.text[0:150]
        article_obj = models.Article.objects.create(
            title=title,
            content=str(soup),
            desc=desc,
            category_id=category_id,
            blog=request.user.blog
        )
        # 批量插入数据(标签可能有多个)
        article_obj_list = []
        for tag_id in tag_id_list:
            tag_article_obj = models.Article2Tag(article=article_obj,tag_id=tag_id)
            article_obj_list.append(tag_article_obj)
        models.Article2Tag.objects.bulk_create(article_obj_list)
        #跳转到后台管理文章展示页
        return redirect('/backend/')
    #当前文章的所属分类和标签
    category_list = models.Category.objects.filter(blog=request.user.blog)
    tag_list = models.Tag.objects.filter(blog=request.user.blog)
    return render(request,'backend/add_article.html',locals())


def upload_image(request):
    '''
    //成功时
    {
            "error" : 0,
            "url" : "http://www.example.com/path/to/file.ext"
    }
    //失败时
    {
            "error" : 1,
            "message" : "错误信息"
    }
    :param request:
    :return:
    '''
    if request.method == 'POST':
        #先定义返回给编辑器的数据格式
        back_dict = {'error':0}
        #获取用户上传的图片对象
        file_obj = request.FILES.get('imgFile')
        #手动拼接存储文件的路径
        file_dir = os.path.join(settings.BASE_DIR,'media/app01','article_img')
        #优化操作:先判断当前文件夹是否存在，如果不存在则自动创建
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        #拼接图片的完整路径
        file_path = os.path.join(file_dir,file_obj.name)
        with open(file_path,'wb') as f:
            for line in file_obj:
                f.write(line)
        back_dict['url'] = f'/media/app01/article_img/{file_obj.name}'
    return JsonResponse(back_dict)


@login_required
def set_avatar(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar')
        #不会自动把头像添加至avatar文件夹中
        models.UserInfo.objects.filter(pk=request.user.pk).update(avatar=file_obj)
        request.user.avatar = file_obj
        request.user.save()
        return redirect('/home/')
    blog = request.user.blog
    username = request.user.username
    return render(request,'set_avatar.html',locals())

