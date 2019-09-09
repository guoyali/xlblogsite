# coding:utf-8
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

#如果登录则转到登录页面
def islogin(func):
    def login_fun(request,*args,**kwargs):
        if request.session.get('user_id'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/article/login')
            red.set_cookie('url',request.get_full_path)
            return red
    return login_fun