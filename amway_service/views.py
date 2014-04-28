
import json, logging
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

from django.http import HttpResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from common.util.nice_http_util import get_client_ip

CONFERENCE_LOG_PATH = './logs/conference'
isExists = os.path.exists(CONFERENCE_LOG_PATH)
if not isExists:
    os.makedirs(CONFERENCE_LOG_PATH)


def index(request):
    return HttpResponse('', content_type="text/html")

@csrf_exempt
def conference_survey(request):
    result = 1
    try:
        ip = get_client_ip(request)
        log_filehandler = open(CONFERENCE_LOG_PATH + '/conference_survey.'
                               + datetime.now().strftime('%Y-%m-%d') + '.log', 'a')

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

        conference_survey = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s' % \
                         (ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          str(name), srid, identity, telephone, answer1, answer2,
                          answer3, answer4, answer5, answer6, surveylocation, '\n')
        print conference_survey
        # print user_login_log
        log_filehandler.write('%s' % conference_survey)
        result = 1
    except Exception, e:
        logging.error(e)
        logging.error(request)
        result = 0
    finally:
        log_filehandler.close()


    response_data = {}
    response_data['result'] = result
    response_data['data'] = {}
    return HttpResponse(json.dumps(response_data), content_type="application/json")