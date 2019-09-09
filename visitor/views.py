#coding=utf8
from django.db.models import Q
from article.views import *
import time
import markdown


@csrf_exempt
def article_list(request,page):
    '''文章展示'''
    print '博客首页'
    s = request.get_full_path()
    s = str(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    post_info = request.POST
    search = post_info.get('search')
    column = post_info.get('column')
    articles = Article.objects.all()
    if search:
        author = User.objects.filter(username=search)
        articles = articles.filter(Q(uid__in=[i.id for i in author])|
                                   Q(title__contains=search))
    context = []
    if column:
        articles = articles.filter(cid=column)
    articles = articles.order_by('weight','-uptime')
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

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
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j ='article_{}'.format(i+1)
        b.append(j)
    context_c = zip(a,b)

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id,i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid,i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid,i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        uid = i.uid
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        # summary = i.summary
        summary = markdown.markdown(
            i.content[0:175]+'.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                     'content': content, 'summary': summary, 'addtime': addtime,
                     'like_num': like_num, 'comment_count': comment_count,'uid': uid,'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i+1)
    try:
        aid_t1 = TopArticle.objects.all().order_by('-id')[0].aid
        article_t = Article.objects.get(aid=aid_t1)
        uid_t = article_t.uid
        aid_t = article_t.aid
        cid_t = article_t.cid
        author = User.objects.get(id=uid_t).username
        column = ArticleColumn.objects.get(cid=cid_t).column_name
        title = article_t.title
        content = article_t.content
        # summary = i.summary
        summary = markdown.markdown(
            article_t.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )

        addtime = article_t.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = LikeCount.objects.get(aid=aid_t).count

        comment_count = UserComment.objects.filter(aid=aid_t).count()
        context_top = {'aid': aid_t, 'author': author, 'column': column, 'title': title,
                            'content': content, 'summary': summary, 'addtime': addtime,
                            'like_num': like_num, 'comment_count': comment_count, 'uid': uid_t, 'cid': cid_t}
        return render(request, 'article_list.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c, 'context_top': context_top
                                                 })  # 博客首页展示
    except:
        return render(request, 'article_list1.html', {'context': context,'page_num': pages,'pindex':pindex,
                                                 'context_c': context_c})  # 博客首页展示


@csrf_exempt
def top(request):
    '''置顶文章展示'''
    aid_t1 = TopArticle.objects.all().order_by('-id')[0].aid
    article_t = Article.objects.get(aid=aid_t1)
    context_top = []

    uid_t = article_t.uid
    aid_t = article_t.aid
    cid_t = article_t.cid
    author = User.objects.get(id=uid_t).username
    column = ArticleColumn.objects.get(cid=cid_t).column_name
    title = article_t.title
    content = article_t.content
    # summary = i.summary
    summary = markdown.markdown(
        article_t.content[0:175] + '.....',
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    # summary = summary+"..."

    addtime = article_t.addtime
    addtime = time.localtime(int(addtime))
    addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
    like_num = ArticleLike.objects.filter(aid=aid_t).count()
    comment_count = UserComment.objects.filter(aid=aid_t).count()
    context_top.append({'aid': aid_t, 'author': author, 'column': column, 'title': title,
                    'content': content, 'summary': summary, 'addtime': addtime,
                    'like_num': like_num, 'comment_count': comment_count, 'uid': uid_t, 'cid': cid_t})
    print context_top
    return render(request,'article_list.html',{'context_top': context_top})




@csrf_exempt
def article_detail(request,aid):
    '''文章内容'''
    print '文章详情'
    # aid = request.GET.get('aid')
    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    aid = s.split('/')[2].split('.')[0]
    print aid
    article = Article.objects.get(aid=aid)
    context = []
    comments = []

    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    title = article.title
    aid = article.aid
    uid = article.uid
    cid = article.cid
    author = User.objects.get(id=uid).username
    addtime = article.addtime
    addtime = time.localtime(int(addtime))
    addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
    comment_count = UserComment.objects.filter(aid=aid).count()
    like_num = LikeCount.objects.get(aid=aid).count
    comment_user = UserComment.objects.filter(aid=aid)
    content = markdown.markdown(
        article.content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    if comment_user:
        for i in comment_user:
            conment_username = i.comment_name
            comment_content = i.content
            conment_addtime = i.addtime
            conment_addtime = time.localtime(int(conment_addtime))
            conment_addtime = time.strftime("%Y-%m-%d %H:%M:%S", conment_addtime)
            comments.append({'conment_username': conment_username,'comment_content': comment_content,'conment_addtime':conment_addtime})
    context.append({'author':author,'title':title, 'content':content, 'addtime': addtime,'comment_count': comment_count,
                    'like_num': like_num,'aid':aid,'cid': cid})
    return render(request, 'detail.html', {'context': context[0], 'context_c':context_c,'comments': comments,'aid':aid,'uid':uid})  # 博客详情页展示


@csrf_exempt
def add_comment(request):
    '''新增文章评论'''
    post_info = request.POST
    aid = request.GET.get('aid')
    cid = request.GET.get('cid')
    comment_name = post_info.get('comment_name')
    content = post_info.get('content')
    conment = UserComment.objects.create(aid=aid,comment_name=comment_name,content=content)
    conment.save()
    return HttpResponseRedirect('/article_detail/{}.html'.format(aid))


@csrf_exempt
def reply_comment(request):
    '''回复评论'''
    post_info = request.POST
    aid = request.GET.get('aid')
    rid = request.GET.get('rid')
    comment_name = post_info.get('comment_name')
    content = post_info.get('content')
    comment = ReplyComment.objects.create(rid=rid,comment_name=comment_name,content=content)
    comment.save()
    return HttpResponseRedirect('/article_detail/?aid={}'.format(aid))


@csrf_exempt
def like_article(request):
    '''新增文章点赞功能'''
    aid = request.GET.get('aid')
    if aid:
        likecount = LikeCount.objects.get(aid=aid)
        count = likecount.count + 1
        likecount.count = count
        likecount.save()
        # data = {"data":True}
        # return JsonResponse(data)
        return HttpResponse(json.dumps({'data': True}), content_type='application/json')

    else:
        data = {"data": False}
        # return JsonResponse(data)
        return HttpResponse(json.dumps({'data': False}), content_type='application/json')


@csrf_exempt
def author_article(request,uid,page):
    # uid = request.GET.get('uid')
    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    uid = s.split('/')[2]
    pindex = s.split('/')[3].split('.')[0].split('p')[1]

    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1
    articles = Article.objects.filter(uid=uid)
    articles = articles.order_by('-addtime')
    cids = articles.values_list('cid', flat=True)
    column = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    context = []

    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    for i in articles:
        aid = i.aid
        cid = i.cid
        title = i.title
        content = i.content
        # summary = i.summary
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        column_name = column.get(cid)
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        context.append({'cid': cid, 'aid': aid, 'title': title, 'content': content, 'column_name': column_name,
                        'addtime': addtime,'summary':summary})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request,'author_article.html',{'context':context,'context_c': context_c,'uid':uid,'page_num': pages,'pindex':pindex})


@csrf_exempt
def column_1(request,page):
    context = []
    post_info = request.POST
    page = int(post_info.get('page', 1))
    page_size = int(post_info.get('page_size', 10))
    start = max((page - 1), 0) * page_size
    end = page * page_size

    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    column_id = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        column_id.append(ArticleColumn.objects.get(cid=i).cid)
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    cid = column_id[0]
    articles = Article.objects.filter(cid=cid)
    articles = articles.order_by('-uptime')
    articles = articles[start:end]


    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id, i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid, i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                        'content': content, 'summary': summary, 'addtime': addtime,
                        'like_num': like_num, 'comment_count': comment_count, 'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request, 'article_1.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c,

                                                 })  # 博客首页展示


@csrf_exempt
def column_2(request,page):
    context = []
    post_info = request.POST
    page = int(post_info.get('page', 1))
    page_size = int(post_info.get('page_size', 10))
    start = max((page - 1), 0) * page_size
    end = page * page_size
    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    column_id = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        column_id.append(ArticleColumn.objects.get(cid=i).cid)
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    cid = column_id[1]
    articles = Article.objects.filter(cid=cid)
    articles = articles.order_by('-uptime')
    articles = articles[start:end]
    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id, i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid, i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                        'content': content, 'summary': summary, 'addtime': addtime,
                        'like_num': like_num, 'comment_count': comment_count, 'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request, 'article_2.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c,

                                                 })  # 博客首页展示


@csrf_exempt
def column_3(request,page):
    context = []
    post_info = request.POST
    page = int(post_info.get('page', 1))
    page_size = int(post_info.get('page_size', 10))
    start = max((page - 1), 0) * page_size
    end = page * page_size
    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    column_id = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        column_id.append(ArticleColumn.objects.get(cid=i).cid)
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    cid = column_id[2]
    articles = Article.objects.filter(cid=cid)
    articles = articles.order_by('-uptime')
    articles = articles[start:end]
    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id, i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid, i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                        'content': content, 'summary': summary, 'addtime': addtime,
                        'like_num': like_num, 'comment_count': comment_count, 'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request, 'article_3.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c,

                                                 })  # 博客首页展示


@csrf_exempt
def column_4(request,page):
    context = []
    post_info = request.POST
    page = int(post_info.get('page', 1))
    page_size = int(post_info.get('page_size', 10))
    start = max((page - 1), 0) * page_size
    end = page * page_size
    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    column_id = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        column_id.append(ArticleColumn.objects.get(cid=i).cid)
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    cid = column_id[3]
    articles = Article.objects.filter(cid=cid)
    articles = articles.order_by('-uptime')
    articles = articles[start:end]
    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)
    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id, i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid, i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                        'content': content, 'summary': summary, 'addtime': addtime,
                        'like_num': like_num, 'comment_count': comment_count, 'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request, 'article_4.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c,

                                                 })  # 博客首页展示


@csrf_exempt
def column_5(request,page):
    '''redis'''
    context = []
    post_info = request.POST
    page = int(post_info.get('page', 1))
    page_size = int(post_info.get('page_size', 10))
    start = max((page - 1), 0) * page_size
    end = page * page_size
    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    column_id = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        column_id.append(ArticleColumn.objects.get(cid=i).cid)
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    cid = column_id[4]
    articles = Article.objects.filter(cid=cid)
    articles = articles.order_by('-uptime')
    articles = articles[start:end]
    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id, i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid, i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                        'content': content, 'summary': summary, 'addtime': addtime,
                        'like_num': like_num, 'comment_count': comment_count, 'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request, 'article_5.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c,

                                                 })  # 博客首页展示


@csrf_exempt
def column_6(request,page):
    '''mongo'''
    context = []
    post_info = request.POST
    page = int(post_info.get('page', 1))
    page_size = int(post_info.get('page_size', 10))
    start = max((page - 1), 0) * page_size
    end = page * page_size
    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    column_id = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        column_id.append(ArticleColumn.objects.get(cid=i).cid)
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    cid = column_id[5]
    articles = Article.objects.filter(cid=cid)
    articles = articles.order_by('-uptime')
    articles = articles[start:end]
    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id, i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid, i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                        'content': content, 'summary': summary, 'addtime': addtime,
                        'like_num': like_num, 'comment_count': comment_count, 'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request, 'article_6.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c,

                                                 })  # 博客首页展示


@csrf_exempt
def column_7(request,page):
    '''开发工具'''
    context = []
    post_info = request.POST
    page = int(post_info.get('page', 1))
    page_size = int(post_info.get('page_size', 10))
    start = max((page - 1), 0) * page_size
    end = page * page_size
    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    column_id = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        column_id.append(ArticleColumn.objects.get(cid=i).cid)
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    cid = column_id[6]
    articles = Article.objects.filter(cid=cid)
    articles = articles.order_by('-uptime')
    articles = articles[start:end]
    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id, i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid, i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                        'content': content, 'summary': summary, 'addtime': addtime,
                        'like_num': like_num, 'comment_count': comment_count, 'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request, 'article_7.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c,

                                                 })  # 博客首页展示


@csrf_exempt
def column_8(request,page):
    '''vue.js'''
    context = []
    post_info = request.POST
    page = int(post_info.get('page', 1))
    page_size = int(post_info.get('page_size', 10))
    start = max((page - 1), 0) * page_size
    end = page * page_size
    sort = SortColumn.objects.all().order_by('-id')[0].sort
    sort = sort.split('[')[1]
    sort = sort.split(']')[0]
    sort = sort.split(',')
    sorts = []
    column_id = []
    for i in sort:
        sorts.append(int(i))
    columns = []
    for i in sorts:
        column_id.append(ArticleColumn.objects.get(cid=i).cid)
        columns.append(ArticleColumn.objects.get(cid=i).column_name)

    cid = column_id[7]
    articles = Article.objects.filter(cid=cid)
    articles = articles.order_by('-uptime')
    articles = articles[start:end]
    a = []
    b = []
    for i in columns:
        a.append(i)

    for i in range(len(columns)):
        j = 'article_{}'.format(i + 1)
        b.append(j)
    context_c = zip(a, b)

    s = request.get_full_path()
    s = str(s)
    print s
    print type(s)
    pindex = s.split('/')[2].split('.')[0].split('p')[1]
    if pindex:
        pindex = int(pindex)
    else:
        pindex = 1

    uids = []
    cids = []
    aids = []
    for i in articles:
        uids.append(i.uid)
        cids.append(i.cid)
        aids.append(i.aid)
    authors = dict([(i.id, i.real_name) for i in User.objects.filter(id__in=uids)])
    columns = dict([(i.cid, i.column_name) for i in ArticleColumn.objects.filter(cid__in=cids)])
    likes = dict([(i.aid, i.count) for i in LikeCount.objects.filter(aid__in=aids)])

    for i in articles:
        aid = i.aid
        cid = i.cid
        author = authors.get(i.uid)
        column = columns.get(i.cid)
        title = i.title
        content = i.content
        summary = markdown.markdown(
            i.content[0:175] + '.....',
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        addtime = i.addtime
        addtime = time.localtime(int(addtime))
        addtime = time.strftime("%Y-%m-%d %H:%M:%S", addtime)
        like_num = likes.get(i.aid)
        comment_count = UserComment.objects.filter(aid=aid).count()
        context.append({'aid': aid, 'author': author, 'column': column, 'title': title,
                        'content': content, 'summary': summary, 'addtime': addtime,
                        'like_num': like_num, 'comment_count': comment_count, 'cid': cid})
    paginator = Paginator(context, 5)
    context = paginator.page(pindex).object_list
    page_num = paginator.num_pages
    pages = []
    for i in range(page_num):
        pages.append(i + 1)
    return render(request, 'article_8.html', {'context': context, 'page_num': pages, 'pindex': pindex,
                                                 'context_c': context_c,
                                                 })  # 博客首页展示

