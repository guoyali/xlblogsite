# coding:utf-8
__author__ = 'qinman'
# create by qinman on 2017/12/2

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogsite.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()