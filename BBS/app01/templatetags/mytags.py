from  django import template
from app01 import models
from django.db.models import Count
from django.db.models.functions import TruncMonth


register = template.Library()
#自定义inclusion_tag
@register.inclusion_tag('left_menu.html')
def left_menu(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    # 查询当前用户所有的分类及分类下的文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list(
        'name', 'count_num', 'pk')
    # print(category_list)<QuerySet [('Barry的分类一', 2), ('Barry的分类二', 1), ('Barry的分类三', 1)]>
    # 查询当前用户所有的标签及标签下的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list('name',
                                                                                                         'count_num',
                                                                                                         'pk')
    # 按年月统计当前用户的所有的文章
    date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count_num=Count('pk')).values_list('month', 'count_num')
    return locals()