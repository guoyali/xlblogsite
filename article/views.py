# coding=utf8
import hashlib
import random
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.encoding import filepath_to_uri
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
import upyun
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from islogin import *
from models import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



@csrf_exempt
def login(request):
    '''登录页面'''
    return render(request, 'admin/login.html')


@csrf_exempt
def login_handle(request):
    '''接受登录信息'''
    post_info = request.POST
    username = post_info.get('username')
    password = post_info.get('password')
    try:
        user = authenticate(username=username, password=password)
        uid = user.id
        # request.session['is_login'] = True
        request.session['user'] = user
        request.session["uid"] = uid
        articles = Article.objects.filter(uid=uid)
        context = []
        for i in articles:
            title = i.title
            aid = i.aid
            content = i.content
            context.append({'title': title, 'aid': aid, 'content': content})
        return HttpResponseRedirect('/info/{}/p{}.html'.format(uid,1))
        # return render(request, 'admin/info.html')
    except:
        print 456
        return render(request, 'admin/login.html', {'error': '账号密码错误'})


@csrf_exempt
def quit(request):
    print 1111111
    '''退出登录'''
    try:
        uid = request.session['uid']
        print uid
        del request.session['uid']
        print 2222
        # return JsonResponse({'data': True})
        return HttpResponse(json.dumps({'data': True}), content_type='application/json')

    except:
        # return JsonResponse({'data': False})
        return HttpResponse(json.dumps({'data': False}), content_type='application/json')


@csrf_exempt
def info(request,uid,page):
    '''个人文章详情页'''
    # uid = request.GET.get('uid')
    s = request.get_full_path()
    s = str(s)
    uid = s.split('/')[2]
    if int(uid) == int(request.session['uid']):
        username = User.objects.get(id=uid).username
        print username
        post_info = request.POST
        pindex = s.split('/')[3].split('.')[0].split('p')[1]
        # articles = Article.objects.filter(uid=uid)
        articles = Article.objects.all()
        search_title = post_info.get('title'.strip(),"")
        search_column = post_info.get('cid'.strip(), 0)
        if search_title:
            articles = articles.filter(title__icontains=search_title)
        if search_column:
            if int(search_column) != 0:
                search_column = int(search_column)
                articles = articles.filter(cid=search_column)

        if pindex:
            pindex = int(pindex)
        else:
            pindex = 1

        columns = ArticleColumn.objects.all()
        context_c = []
        for i in columns:
            cid = i.cid
            sort = i.sort
            num = Article.objects.filter(cid=cid).count()
            column_name = i.column_name
            context_c.append({'column_name': column_name, 'cid': cid, 'num': num, 'sort': sort})

        articles = articles.order_by('weight', '-uptime')
        cids = articles.values_list('cid', flat=True)
        column = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
        context = []
        for i in articles:
            aid = i.aid
            cid = i.cid
            title = i.title
            weight = i.weight
            content = i.content
            summary = i.summary
            column_name = column.get(cid)
            addtime = i.addtime
            addtime = time.localtime(int(addtime))
            addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
            context.append(
                {'cid': cid, 'aid': aid, 'title': title, 'content': content,'column_name': column_name, 'addtime': addtime,
                 'summary': summary,'weight': weight})
        paginator = Paginator(context, 15)
        context = paginator.page(pindex).object_list
        page_num = paginator.num_pages
        pages = []
        for i in range(page_num):
            pages.append(i + 1)
        return render(request, 'admin/info.html', {'context': context,'context_c': context_c, 'uid': uid, 'title': search_title,
                                               'cid': search_column,'page_num': pages,'pindex':pindex,'username': username})
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def article_info(request,aid,uid,cid):
    '''文章详情'''
    print 1111111
    s = request.get_full_path()
    s = str(s)
    print s
    # print type(s)
    # uid = s.split('/')[2].split('.')[0]
    aid = request.GET.get('aid')
    cid = request.GET.get('cid')
    uid = request.GET.get('uid')
    username = User.objects.get(id=uid).username
    print aid
    print cid
    print uid
    article = Article.objects.get(aid=aid)
    cids = article.values_list('cid', flat=True)
    column = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    context = []
    aid = article.aid
    cid = article.cid
    title = article.title
    content = article.content
    weight = article.weight
    column_name = column.get(cid)
    addtime = article.addtime
    addtime = time.localtime(int(addtime))
    addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
    context.append({'cid': cid, 'aid': aid, 'title': title, 'content': content, 'column_name': column_name,
                    'addtime': addtime,'username': username,'weight': weight})
    print 222222222
    print aid
    print cid
    print uid
    return render(request, '/edit_article/?aid={}&cid={}&uid={}'.format(aid, cid, uid), {'context': context})


@csrf_exempt
def edit_article(request,uid,cid,aid):
    '''编辑文章'''
    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    aid = s.split('/')[2]
    uid = s.split('/')[4].split('.')[0]
    # uid = request.GET.get('uid')
    if int(uid) == int(request.session['uid']):
        columns = ArticleColumn.objects.all()
        context_c = []
        for i in columns:
            _cid = i.cid
            sort = i.sort
            num = Article.objects.filter(cid=_cid).count()
            column_name = i.column_name
            context_c.append({'column_name': column_name, 'cid': _cid, 'num': num, 'sort': sort})
        cid = request.GET.get('cid')
        article = Article.objects.get(aid=aid)
        username = User.objects.get(id=uid).username
        context = []
        aid = article.aid
        print aid
        cid = article.cid
        title = article.title
        weight = article.weight
        content = article.content
        column_name = ArticleColumn.objects.get(cid=cid).column_name
        addtime = article.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        context.append({'cid': cid, 'aid': aid, 'title': title, 'content': content, 'column_name': column_name,
                        'addtime': addtime,'weight': weight})
        print context
        print 789
        return render(request, 'admin/edit.html', {'context': context[0],'context_c': context_c, 'uid': uid,'username': username})
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def edit_article_handle(request,uid,aid):
    '''接受编辑信息'''
    post_info = request.POST
    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    aid = s.split('/')[2]
    uid = s.split('/')[3].split('.')[0]
    username = User.objects.get(id=uid).username
    search_title = post_info.get('title')
    search_cid = post_info.get('cid')
    search_content = post_info.get('content')
    search_img = post_info.get('img')
    search_weight = post_info.get('weight')
    print aid
    print search_title
    print search_cid
    print search_content
    try:
        article = Article.objects.get(aid=aid)
        article.title = search_title
        article.cid = search_cid
        article.weight = search_weight
        article.content = search_content
        if search_img:
            article.image = request.FILES.get('img')
        article.save()
        # return HttpResponseRedirect('/visitor/article_detail/?aid={}'.format(aid))
        return HttpResponseRedirect('/info/{}/p1.html'.format(uid))
    except:
        return render(request, 'admin/edit.html',{'username': username})  # 文章列表页


@csrf_exempt
def add_article(request,uid):
    '''新增文章页面'''
    print 123456
    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    uid = s.split('/')[2].split('.')[0]
    print uid
    if int(uid) == int(request.session['uid']):
        columns = ArticleColumn.objects.all()
        context_c = []
        for i in columns:
            cid = i.cid
            sort = i.sort
            num = Article.objects.filter(cid=cid).count()
            column_name = i.column_name
            context_c.append({'column_name': column_name, 'cid': cid, 'num': num, 'sort': sort})
        username = User.objects.get(id=uid).username
        return render(request, 'admin/add_article.html',{'username': username,'uid': uid,'context_c': context_c})
    else:
        return HttpResponseRedirect('/login/')



@csrf_exempt
def add_article_handle(request,uid):
    '''新增文章信息'''
    post_info = request.POST
    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    uid = s.split('/')[2].split('.')[0]
    title = post_info.get('title')
    content = post_info.get('content')
    cid = post_info.get('cid')
    search_img = post_info.get('img')
    weight = post_info.get('weight')

    if title and content and cid:
        article = Article.objects.create(uid=uid, title=title, content=content, cid=cid)
        if weight:
            article.weight = weight

        article.save()
        aid = article.aid
        likecount = LikeCount.objects.create(aid=aid, count=0)
        likecount.save()
        return HttpResponseRedirect('/info/{}/p1.html'.format(uid))
    else:
        return render(request, 'admin/add_article.html', {'error': '信息不完整'})


@csrf_exempt
def del_article(request):
    '''删除文章'''
    aid = request.GET.get('aid')
    uid = request.GET.get('uid')
    print aid
    print uid
    title = Article.objects.get(aid=aid)
    title.delete()
    print 12344321
    # return JsonResponse({'data': True})
    return HttpResponse(json.dumps({'data': True}), content_type='application/json')


@csrf_exempt
def search(request):
    '''搜索文章'''
    post_info = request.POST
    search_title = post_info.get('title'.strip())
    search_column = post_info.get('cid'.strip(), 0)
    articles = Article.objects.all()
    context = []
    if search_title:
        articles = articles.filter(title__icontains=search_title)
    if search_column:
        if int(search_column) != 0:
            search_column = int(search_column)
            articles = articles.filter(cid=search_column)
    articles = articles.order_by('-uptime')
    count = articles.count()
    for i in articles:
        title = i.title
        aid = i.aid
        uid = i.uid
        cid = i.cid
        column_name = ArticleColumn.objects.get(cid=cid).column_name
        context.append({'title': title, 'column_name': column_name, 'cid': cid, 'aid': aid, 'uid': uid})
    print search_title
    print search_column
    return render(request, 'admin/info.html', {'context': context, 'count': count, 'search_column': search_column,
                                               'search_title': search_title})


def md5(str):
    return  hashlib.md5(str).hexdigest()

class UpyunStorage(Storage):
    "upyun storage"

    BUCKETNAME = settings.UPYUN_BUCKETNAME
    USERNAME = settings.UPYUN_USERNAME
    PASSWORD = settings.UPYUN_PASSWORD
    BASE_URL = settings.UPYUN_BASE_URL
    up = upyun.UpYun(BUCKETNAME, USERNAME, PASSWORD, timeout=30,
                                        endpoint=upyun.ED_AUTO)

    def _save(self, name, content):
        if  name[0] != '/':
            name = "/" + name
        try:
            res = self.up.put(name, content.read(), checksum=False)
            print res
        except Exception as e:
            raise
        return name

    def exists(self, name):
        try:
            self.up.getinfo(name)
        except Exception:
            return False
        return True

    def url(self, name):
        return self.BASE_URL+filepath_to_uri(name)

    @classmethod
    def simple_upload(cls,full_path_name,file_content):
        try:
            res = cls.up.put(full_path_name, file_content, checksum=False)
            print res
        except Exception as e:
            raise
        return cls.BASE_URL+filepath_to_uri(full_path_name)


import re
@csrf_exempt
def upload_picture(request):
    '''上传图片到又拍云'''
    # 请求方法为POST时，进行处理
    if request.method == "POST":
        upfile = request.FILES['editormd-image-file']
        print upfile.name
        print 000000
        code = random.sample(['1', '2', '3', '5', '6', '7', '8', '9', '6', '6', '6', '6', '8', '8', '8', '8'], 6)
        c = ''.join(code)
        upfile.name = c
        print upfile.name
        image = request.FILES['editormd-image-file']
        if image is None:
            return HttpResponse(json.dumps({
                  'success': 0,
                  'message': 'message',
                  'url': ''
                }), content_type='application/json')

        else:
            prefix = md5(str(time.time() + random.random()))
            url =  UpyunStorage.simple_upload('/media/test/%s_%s' % (prefix, upfile.name), upfile.read())
            return HttpResponse(json.dumps({
                  'success': 1,
                  'message': 'message',
                  'url': (url)
                }), content_type='application/json')
    else:
        return HttpResponse({'error'})


@csrf_exempt
def del_column(request):
    '''删除分类'''
    cid = request.GET.get('cid')
    uid = request.GET.get('uid')
    column = ArticleColumn.objects.get(cid=cid)
    column.delete()

    old_sort = SortColumn.objects.all().order_by('-id')[0]
    sort_ = old_sort.sort
    sort_ = sort_.split('[')[1]
    sort_ = sort_.split(']')[0]
    sort_ = sort_.split(',')
    sorts_ = []
    for i in sort_:
        sorts_.append(int(i))
    sorts_.remove(int(cid))
    new = SortColumn.objects.create(sort=sorts_)
    new.save()

    return HttpResponse(json.dumps({'data': True}), content_type='application/json')


@csrf_exempt
def column_list(request,uid):
    '''分类页面'''
    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    uid = s.split('/')[2].split('.')[0]
    if int(uid) == int(request.session['uid']):
        username = User.objects.get(id=uid).username
        columns = ArticleColumn.objects.all()
        columns = columns.order_by('sort', '-uptime')
        context = []

        sort = SortColumn.objects.all().order_by('-id')[0].sort
        sort = sort.split('[')[1]
        sort = sort.split(']')[0]
        sort = sort.split(',')
        sorts = []
        for i in sort:
            sorts.append(int(i))
        print type(sorts)
        columns = []
        for i in sorts:
            columns.append(ArticleColumn.objects.get(cid=i))


        for i in columns:
            cid = i.cid
            sort = i.sort
            num = Article.objects.filter(cid=cid).count()
            column_name = i.column_name
            context.append({'column_name': column_name,'cid': cid,'num': num,'sort': sort})
        return render(request,'admin/column.html',{'context': context,'uid': uid,'username': username})
    else:
        return HttpResponseRedirect('/login/')




@csrf_exempt
def add_column(request,uid):
    '''新增分类'''
    post_info = request.POST
    s = request.get_full_path()
    s = str(s)
    uid = s.split('/')[2].split('.')[0]
    if int(uid) == int(request.session['uid']):
        column_name = post_info.get('column_name')
        columns = ArticleColumn.objects.all().values_list('column_name',flat=True)
        if column_name in columns:
            print 11111111
            return HttpResponse(json.dumps({'data': False}), content_type='application/json')
        else:
            column = ArticleColumn.objects.create(column_name=column_name,sort=1000)
            print 22222222
            column.save()
            old_sort = SortColumn.objects.all().order_by('-id')[0]
            sort_ = old_sort.sort
            sort_ = sort_.split('[')[1]
            sort_ = sort_.split(']')[0]
            sort_ = sort_.split(',')
            sorts_ = []
            for i in sort_:
                sorts_.append(int(i))
            print sorts_
            print type(sorts_)
            print column.cid
            sorts_.append(int(column.cid))
            new = SortColumn.objects.create(sort=sorts_)
            new.save()
        return HttpResponseRedirect('/column_list/{}.html'.format(uid))
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def top_article(request):
    '''文章置顶'''
    post_info = request.POST
    aid = post_info.get('aid')
    top = TopArticle.objects.create(aid=aid,first=1)
    top.save()
    return HttpResponse(json.dumps({'data': True}), content_type='application/json')


@csrf_exempt
def get_column(request):
    '''接收目录排序'''
    print 111
    sort_id = request.GET.get('ids')
    print sort_id
    try:
        sort = SortColumn.objects.create(sort=sort_id)
        sort.save()
        return HttpResponse(json.dumps({'data': True}), content_type='application/json')
    except Exception as e:
        print e




