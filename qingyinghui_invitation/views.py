# -*- coding:utf-8 -*-
# Create your views here.
import urllib
from django.core.exceptions import ObjectDoesNotExist

from django.template import RequestContext
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.shortcuts import render_to_response
import json
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def index(request):
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def myinvitation(request):
    return render_to_response('myinvitation.html', locals(), context_instance=RequestContext(request))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def login(request):
    #TODO 记录 ip 时间   卡号  id  到文件中， 便于日后统计。
    try:
        ip = get_client_ip(request)
        log_filehandler = open('./invitation_user_login.log' + datetime.now().strftime('%Y-%m-%d') + '.log', 'a')
        user_no = request.POST['ada']
        user_name = request.POST['name']
        user_login_log = '%s\t%s\t%s\t%s%s' % (ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                               str(user_no), user_name, '\n')
        # print user_login_log
        log_filehandler.write('%s' % user_login_log)
    except:
        print 'error:', request
        print sys.exc_info()[0]
    finally:
        log_filehandler.close()


    response_data = {}
    response_data['result'] = 1

    user_info = {}
    user_info['ada'] = user_no
    user_info['name'] = user_name
    response_data['data'] = user_info
    return HttpResponse(json.dumps(response_data), content_type="application/json")