from django.db import models

# Create your models here.
'''
先写普通字段，再先外键字段
注意所有的外键字段都会默认加'_id'
'''
from django.contrib.auth.models import AbstractUser


#用户表
class UserInfo(AbstractUser):
    phone = models.BigIntegerField(null=True,blank=True,verbose_name='手机号')
    '''
    null=True 数据库中该字段可以为空
    blank=True admin后台管理中该字段可以为空
    '''
    avatar = models.FileField(upload_to='app01/avatar/',default='avatar/default.png',verbose_name='默认头像')
    '''
    给avatar(头像)字段传文件对象,该文件会自动存储到avatar文件下,然后avatar字段只保存文件文件路径avatar/default
    设置默认头像
    '''
    create_time = models.DateField(auto_now_add=True,verbose_name='创建时间')
    blog = models.OneToOneField(to='Blog',null=True)
    #修改admin后台管理的表名
    class Meta:
        verbose_name_plural = '用户表'
    def __str__(self):
        return self.username

#个人站点表
class Blog(models.Model):
    site_name = models.CharField(max_length=32,verbose_name='站点名称')
    site_title = models.CharField(max_length=32,verbose_name='站点标题')
    site_theme = models.CharField(max_length=64,verbose_name='站点样式')
    class Meta:
        verbose_name_plural = '个人站点表'
    def __str__(self):
        return self.site_theme

#文章分类表
class Category(models.Model):
    name = models.CharField(max_length=32,verbose_name='文章分类')
    blog = models.ForeignKey(to='Blog',null=True)
    class Meta:
        verbose_name_plural = '文章分类表'
    def __str__(self):
        return self.name

#文章标签表
class Tag(models.Model):
    name = models.CharField(max_length=32,verbose_name='文章标签')
    blog = models.ForeignKey(to='Blog', null=True)
    class Meta:
        verbose_name_plural = '文章标签表'
    def __str__(self):
        return self.name

#文章表
class Article(models.Model):
    title = models.CharField(max_length=64,verbose_name='文章标题')
    desc = models.CharField(max_length=255,verbose_name='文章简介')
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateField(auto_now_add=True,verbose_name='创建时间')
    #数据库字段优化
    up_num = models.BigIntegerField(default=0,verbose_name='点赞数')
    down_num = models.BigIntegerField(default=0,verbose_name='点踩数')
    comment_num = models.BigIntegerField(default=0,verbose_name='评论数')
    #外键字段
    blog = models.ForeignKey(to='Blog', null=True)
    category = models.ForeignKey(to='Category',null=True)
    #tags为多对多外键字段
    tags = models.ManyToManyField(to='Tag',
                                 through='Article2Tag',
                                 through_fields=('article','tag')
                                 )
    class Meta:
        verbose_name_plural = '文章表'

    def __str__(self):
        return self.title

#点赞点踩表
class UpAndDown(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    is_up = models.BooleanField() #传布尔值，存0/1
    class Meta:
        verbose_name_plural = '点赞点踩表'

#评论表
class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    content = models.CharField(max_length=255,verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    #自关联(用于根评论和子评论)
    parent = models.ForeignKey(to='self',null=True)#有些评论只有根评论，该字段可以为空
    class Meta:
        verbose_name_plural = '评论表'

#文章和标签多对多关系表
class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')
    class Meta:
        verbose_name_plural = '文章和标签关系表'