'''
如果项目需要多个forms组件，需要创建一个文件夹，
在文件夹内根据forms组件功能的不同创建不同的py文件
'''
from django import forms
from app01 import models


class MyRegForm(forms.Form):
    username = forms.CharField(label='用户名',min_length=3,max_length=8,
                               error_messages={
                                    'min_length':'用户名最少3位',
                                    'max_length':'用户名最多8位',
                                    'required':'用户名不能为空'
                               },
                               #添加bootstrap样式
                               widget=forms.widgets.TextInput(attrs={'class':'form-control'})
                               )
    password = forms.CharField(label='密码', min_length=3, max_length=8,
                               error_messages={
                                   'min_length': '密码最少3位',
                                   'max_length': '密码最多8位',
                                   'required': '密码不能为空'
                               },
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                               )
    confirm_password = forms.CharField(label='确认密码', min_length=3, max_length=8,
                               error_messages={
                                   'min_length': '确认密码最少3位',
                                   'max_length': '确认密码最多8位',
                                   'required': '确认密码不能为空'
                               },
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                               )
    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'invalid':'邮箱格式不正确',
                                 'required':'邮箱不能为空'
                             },
                             widget=forms.widgets.EmailInput(attrs={'class': 'form-control'})
                             )
    #局部钩子：校验用户名是否已存在
    def clean_username(self):
        #获取用户名
        username = self.cleaned_data.get('username')
        #去数据库中校验
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            self.add_error('username','用户名已存在')
        return username

    #全局钩子：校验两次输入的密码是否一致
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not password == confirm_password:
            self.add_error('confirm_password','两次密码不一致')
        #返回所有数据
        return  self.cleaned_data