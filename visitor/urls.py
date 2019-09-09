# coding:utf-8
from django.conf.urls import patterns, url
from . import views
from blogsite import settings

app_name = 'visitor'

urlpatterns = patterns('',
    # url(r'article/', views.article_list),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATICFILES_DIRS[0]}),
    url(r'^article/p(\d+).html/', views.article_list,name='article'),
    url(r'^like_article_1/$', views.like_article),
    url(r'^article_1/p(\d+).html/', views.column_1,name='article_1'),
    url(r'^article_2/p(\d+).html/', views.column_2,name='article_2'),
    url(r'^article_3/p(\d+).html/', views.column_3,name='article_3'),
    url(r'^article_4/p(\d+).html/', views.column_4,name='article_4'),
    url(r'^article_5/p(\d+).html/', views.column_5,name='article_5'),
    url(r'^article_6/p(\d+).html/', views.column_6,name='article_6'),
    url(r'^article_7/p(\d+).html/', views.column_7,name='article_7'),
    url(r'^article_8/p(\d+).html/', views.column_8,name='article_8'),
    url(r'^article_detail/(\d+).html', views.article_detail,name='article_detail'),
    # url(r'^article_detail/$', views.article_detail),
    url(r'^add_comment/$', views.add_comment),
    url(r'^top/$', views.top),
    # url(r'^article_author/$', views.author_article),
    url(r'^article_author/(\d+)/p(\d+).html', views.author_article, name='author_article'),

    url(r'^column_list/', views.column_list),
                     )