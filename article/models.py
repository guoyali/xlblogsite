# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
import time


class ProfileBase(type):
    def __new__(cls,name,bases,attrs):
        parents = [b for b in bases if isinstance(b,ProfileBase)]
        if parents:
            fields = []
            for obj_name,obj in attrs.items():
                if isinstance(obj,models.Field):fields.append(obj_name)
                User.add_to_class(obj_name,obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name,{'fields':fields}))
        return super(ProfileBase,cls).__new__(cls,name,bases,attrs)


class Profile(object):
    __metaclass__ = ProfileBase


class MyProfile(Profile):
    '''用户模块拓展表'''
    real_name = models.CharField(max_length=100, default='')  # 昵称
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间
    uptime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 更新时间


class Article(models.Model):
    '''博客文章表'''
    aid = models.AutoField(primary_key=True)         # 文章id
    uid = models.PositiveIntegerField(default=0)     # 作者id
    cid = models.PositiveIntegerField(default=0)     # 类别id
    title = models.CharField(max_length=300)         # 题目
    # image = models.ImageField(upload_to="/media/user_image", default='')   # 图片
    content = models.TextField(default='')           # 文章内容
    summary = models.CharField(max_length=300, default='', help_text=u"摘要")       # 文章摘要
    weight = models.PositiveIntegerField(default=0)  #权重排序
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间
    uptime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 更新时间

    class Meta:
        db_table = "article"
        app_label = 'blogsite'


class UserComment(models.Model):
    '''用户评论表'''
    id = models.AutoField(primary_key=True)
    comment_name = models.CharField(max_length=100)      # 评论人姓名
    aid = models.PositiveIntegerField(default=0)         # 文章id
    content = models.TextField(default='')               # 评论内容
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间
    uptime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 更新时间

    class Meta:
        db_table = "user_comment"
        app_label = 'blogsite'

class ReplyComment(models.Model):
    '''回复评论表'''
    id = models.AutoField(primary_key=True)
    rid = models.PositiveIntegerField(default=0)     # 被评论人id
    comment_name = models.CharField(max_length=100)   # 评论人姓名
    content = models.TextField(default='')  # 评论内容
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间
    uptime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 更新时间

    class Meta:
        db_table = "reply_comment"
        app_label = 'blogsite'




class ArticleColumn(models.Model):
    '''类别表'''
    cid = models.AutoField(primary_key=True)    # 类别id
    column_name = models.CharField(max_length=100,default='')     # 分类名称
    sort = models.PositiveIntegerField(default=0)  # 权重排序
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间
    uptime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 更新时间

    class Meta:
        db_table = "article_column"
        app_label = 'blogsite'


class ArticleLike(models.Model):
    '''文章点赞变更表'''
    id = models.AutoField(primary_key=True)
    aid = models.PositiveIntegerField(default=0)     # 文章id
    uid = models.PositiveIntegerField(default=0)     # 读者id
    type = models.PositiveIntegerField(default=0)     # 点赞类型      1 点赞  2 取消点赞
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间
    uptime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 更新时间

    class Meta:
        db_table = "article_like"
        app_label = 'blogsite'


class LikeCount(models.Model):
    '''文章点赞数量'''
    id = models.AutoField(primary_key=True)
    aid = models.PositiveIntegerField(default=0)  # 文章id
    count = models.PositiveIntegerField(default=0)    # 文章点赞总数
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间
    uptime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 更新时间

    class Meta:
        db_table = "like_count"
        app_label = 'blogsite'


class TopArticle(models.Model):
    '''文章置顶'''
    id = models.AutoField(primary_key=True)
    aid = models.PositiveIntegerField(default=0)  # 文章id
    first = models.PositiveIntegerField(default=1) #置顶
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间
    # uptime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 更新时间

    class Meta:
        db_table = "top_article"
        app_label = 'blogsite'


class SortColumn(models.Model):
    '''目录排序'''
    id = models.AutoField(primary_key=True)
    sort = models.CharField(default=0)   # 排序ids
    addtime = models.PositiveIntegerField(default=lambda: int(time.time()))  # 创建时间

    class Meta:
        db_table = "sort_column"
        app_label = 'blogsite'

