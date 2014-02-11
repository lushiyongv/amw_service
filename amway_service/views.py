__author__ = 'zhangliang'

from django.http import HttpResponse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def index(request):
    return HttpResponse('', content_type="text/html")
