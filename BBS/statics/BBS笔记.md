注册功能

```py
1.书写一个注册需要的forms组件
		注意点：有多个forms组件时，需要创建一个文件夹，根据不同功能创建不同的py文件
2.利用forms主键渲染前端标签
		1.采用ajax提交表单
		2.需要用form标签来包含我们所有的获取用户数据的html代码
				$('#myform').serializeArray()
					获取到form标签内所有用户的普通键值对的数据
					[{'name':'username','value':'xxx'},{},{}]
3.手动渲染用户头像的标签
		<label for="myfile">头像
     {% load static %}
          <img src="{% static 'img/default.png' %}" alt="" id="myimg" title="头像"  width="100px" style="margin-left: 20px">
        </label>
        只要是label里面的内容点击都会跳转到for指定的标签上
    4.如何实时展示头像
    	1.利用文件阅读器
    	2.change事件
    	3.onload等待加载完毕
    5.一旦用户数据不合法如何精确的渲染提示信息
    	1.form组件渲染的标签id值都有一个固定的特点
    		id_字段名
    		ps:如何获取id值 -->form.auto_id
    	2.根据后端返回的字段以及字段对应的报错信息，需手动拼接对应字段的id值
    	3.提示功能的完善
    		1.jQuery的链式操作
    		2.input获取焦点事件
```

登陆功能

```py
1.手动搭建获取用户的用户名、密码、验证码的前端标签代码
2.图片验证码如何自己完成（极验科技有滑动认证）
	ps:
		img标签src属性后面可以写的内容
			1.直接写网络图片地址
			2.url后缀（/get_code/）
			3.图片的二进制数据
	1.需要借助pillow模块
		Image ImageDraw ImageFont
	2.需要借助内存管理管理器io模块
	3.字体样式受.ttf结尾的文件控制
	4.需手动产生随机验证码
		random模块	
		chr内置方法
		在session中保存验证码

```

用户头像展示

```py
1.网址所使用的静态文件默认放在static文件夹下
2.用户上传的静态文件也应该单独放在某个文件夹下

media配置
	该配置可以让用户上传的所有文件都固定存放在某一个指定的文件下
	# 配置用户上传的文件存储位置
	MEDIA_ROOT = os.path.join(BASE_DIR,'media')
	
如何开设后端指定文件夹资源
		#暴露后端指定文件夹资源
    #在暴露资源的时候一定要明确该资源是否可以暴露
    	url(r'^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),
```

图片防盗链

```py
	如何避免别的网站直接通过本网站的url访问本网站的资源	
```

首页搭建

```py
利用django.admin后台管理
	在相应app的admin.py中注册
		admin.site.register(models.UserInfo)
数据的绑定：
	1.文章表绑定数据
		个人站点、文章分类
	2.用户和个人站点绑定关系
	3.文章和文章标签绑定关系
```

个人站点

```py
由于url方法的第一个参数是正则表达式，所以当路由特别多的时候，看你会出现被顶替的情况，
正对这种情况有两种解决方式
	1.修改正则表达式
	2.调整url方法的位置
	
1.修改个人站点页面布局为3、9
2.个人站点的每个样式都不一样的实现方法：
	内部给每个人都开设可以自定义css和js的文件接口，
	用户自定义之后会将用户的文件保存下来，
	之后打开用户界面的时候会自动加载用户自己的css和js
	
当一个页面的局部需要在多个页面使用并且还需要传参数，可以自定义inclusion_tag

3.侧边栏展示
	 1.查询当前用户所有的分类及分类下的文章数
	 2.查询当前用户所有的标签及标签下的文章数	
	 3.按年月统计当前用户的所有的文章
	 		需要截取日期 from django.db.models.functions import TruncMonth
	 		时区问题：在settings.py文件中修改时区 
	 			TIME_ZONE = ’Asia/Shanghai‘或USE_TZ = False
	 4.侧边栏的筛选功能
	 		urls设计样式
	 		https://www.cnblogs.com/Barry/tag/1            标签
			https://www.cnblogs.com/Barry/category/1       分类
			https://www.cnblogs.com/Barry/archives/2021/11 日期
	 		多个url公用一个视图函数
	 			
```

文章详情页

```py
	url设计：
		https://www.cnblogs.com/Barry/p/1 
	文章的详情页和个人站点页基本一致，利用模版的继承(base.html)
```

文章点赞点踩

```py
	在浏览器上看到的文章内容，其内部都是html(前端)代码
	如何拷贝文章？
		打开文章页面，右键检查，copy  outerhtml
		需要用到过滤器safe
#前端页面
		1.拷贝点赞点踩
			拷贝前端点赞点踩图标
			拷贝html和css
		2.如何判断用户到底点击了哪个图标
			1.给这两个图标添加一个公共的样式类(action)
			2.给这个公共样式类绑定一个点击事件
			3.再利用this指代当前被操作的对象，利用hasClass判断是否有某个特定的类属性
				(点赞中有diggit类属性，点踩中没有)，从而判断出到底是哪个图标
			4.ajax提交数据
			5.后端逻辑书写完毕后，前端针对点赞点踩动作实现需要动态展示提示信息
					1.Number()把字符串转数字
					2.用户没有登陆需要展示登陆提示html()
#后端逻辑
	1.先判断当前用户是否登陆
	2.判断当前文章是否是当前用户自己写的
	3.判断当前用户是否已经点赞或点踩
		利用article_obj文章对象和request.user用户对象去点赞点踩表中筛选数据，如果有数据则点过
	4.同时操作两张表的数据库（点赞点踩表、文章表中的普通字段）
```

文章评论

```p
	先写根评论
	再写子评论
	
	点击评论按钮需要将评论框内容清空
	根评论的两步渲染方式
		1.DOM临时渲染
		2.页面刷新永久（render）渲染
			后端直接获取当前文章对应的所有评论，传递给html页面
			前端利用for循环，参考博客园样式			
		3.评论中的内容需清空
		
	子评论
		点击回复按钮后发生的事：
			1.评论框自动聚焦 .focus()
			2.将回复按钮所在的那一行评论人的姓名
				@username
			3.评论框内部自动换行
	
	根评论和子评论都是点击一个按钮朝后端提交数据
	根评论和子评论的区别在哪？
		parent_id
		ajax只需添加一个parent_id
		针对子评论要切割出@username内容
		渲染评论楼要判断是否是子评论
```

添加文章

kindeditor 富文本编辑器

```py
	编辑器的种类很多，可以上网搜索
	下载模块 pip3 install beautifulsoup4
	导入模块 from bs4 import BeautifulSoup
```

编辑器上传图片

```py
		编辑器提前写好的接口，需要手动修改
```

BBS总结

```py
	主要功能总结：
		表设计(最重要)
	
```



