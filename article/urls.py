# coding:utf-8
from django.conf.urls import patterns, url
from . import views
from django.conf import settings
app_name = 'article'

urlpatterns = patterns('',
    # url(r'register_handle/', views.register_handle),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATICFILES_DIRS[0]}),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^info/(\d+)/p(\d+).html', views.info,name='info'),
    url(r'^add_column/(\d+).html', views.add_column, name='add_column'),
    url(r'^del_column/$', views.del_column),
    url(r'^column_list/(\d+).html', views.column_list, name='column_list'),
    url(r'^upload_picture/$', views.upload_picture),
    url(r'^quit/$', views.quit),
    url(r'^search/$', views.search),
    url(r'^edit_article/$', views.edit_article),
    url(r'^edit_article/(\d+)/(\d+)/(\d+).html', views.edit_article,name='edit_article'),
    url(r'^del_article/$', views.del_article),
    url(r'^top_article/$', views.top_article),
    url(r'^get_column/$', views.get_column),
    url(r'^add_article/(\d+).html', views.add_article,name='add_article'),
    url(r'^add_article_handle/(\d+).html', views.add_article_handle, name='add_article_handle'),
    url(r'^edit_article_handle/(\d+)/(\d+).html', views.edit_article_handle,name='edit_article_handle'),
                       )