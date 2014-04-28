from django.views.decorators.csrf import csrf_exempt
from common.util.nice_http_util import get_client_ip

import json
from datetime import datetime

from django.http import HttpResponse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def index(request):
    return HttpResponse('', content_type="text/html")

@csrf_exempt
def conference_answer(request):
    result = 1
    try:
        ip = get_client_ip(request)
        log_filehandler = open('./logs/conference_survey.'
                               + datetime.now().strftime('%Y-%m-%d') + '.log', 'a')
        # name:username, srid:srid, identity:userid, telephone:userphone,
        # answer1:ans1, answer2:ans2, answer3:ans3, answer4:ans4,
        # answer5:ans5, answer6:ans6, location:surveylocation,
        name = request.POST['name']
        srid = request.POST['srid']
        identity = request.POST['identity']
        telephone = request.POST['telephone']
        answer1 = request.POST['answer1']
        answer2 = request.POST['answer2']
        answer3 = request.POST['answer3']
        answer4 = request.POST['answer4']
        answer5 = request.POST['answer5']
        answer6 = request.POST['answer6']
        surveylocation = request.POST['surveylocation']

        user_login_log = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s' % \
                         (ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          str(name), srid, identity, telephone, answer1, answer2,
                          answer3, answer4, answer5, answer6, surveylocation, '\n')
        # print user_login_log
        log_filehandler.write('%s' % user_login_log)
        result = 1
    except:
        print 'error:', request
        print sys.exc_info()[0]
        result = 0
    finally:
        log_filehandler.close()


    response_data = {}
    response_data['result'] = result
    response_data['data'] = {}
    return HttpResponse(json.dumps(response_data), content_type="application/json")