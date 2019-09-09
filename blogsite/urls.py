from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from article.models import *
# admin.site.register(Article)
# admin.site.register(UserComment)
# admin.site.register(ArticleColumn)
# admin.site.register(ArticleLike)
# admin.site.register(LikeCount)
from blogsite import settings
from article import views
from django.views.generic import RedirectView

# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATICFILES_DIRS[0]}),
    # Examples:
    # url(r'^$', 'blogsite.views.home', name='home'),
    # url(r'^blogsite/', include('blogsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('article.urls')),
    url(r'', include('visitor.urls')),
    url(r'^$',RedirectView.as_view(url='/article/p1.html/')),
)
