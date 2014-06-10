# -*- coding:utf-8 -*-
import json, logging
import random
import sys, os
from django.shortcuts import render_to_response
from django.template import RequestContext
import qrcode
from amway_service import settings
from conference.models import Survey

reload(sys)
sys.setdefaultencoding('utf-8')

from django.http import HttpResponse
import time
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from common.util.nice_http_util import get_client_ip

CONFERENCE_LOG_PATH = './logs/conference'
isExists = os.path.exists(CONFERENCE_LOG_PATH)
if not isExists:
    os.makedirs(CONFERENCE_LOG_PATH)

DOMAIN = 'http://amway.brixd.com'
# DOMAIN = 'http://0.0.0.0:8000'

#php和静态代码路径/home/wwwroot/www.brixd.com/amway/invitation2014
def index(request):
    return HttpResponse('', content_type="text/html")

@csrf_exempt
def get_reward_status(request):
    result = 1
    try:
        id = request.POST['id']
        survey = Survey.objects.get(pk=id)
    except Exception, e:
        logging.exception(e)
        #失败信息
        result = 0

    response_data = {}

    if survey is None:
        result = 0

    response_data['result'] = result
    if result == 1:
        if survey.reward is True:
            reward = 1
        else:
            reward = 0
        # , survey.srid, survey.name, survey.telephone, reward
        response_data['data'] = {'id':survey.id,'name':survey.name,'telephone':survey.telephone,'reward':reward}
    else:
        response_data['data'] = {}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def conference_reward(request):
    result = 1
    # tips='已经领过了'
    try:
        id = request.POST['id']
        survey = Survey.objects.get(pk=id)
        if survey.reward is False:#成功信息
            pass
            survey.reward=True
            survey.save()
            # tips='尚未领取'
        else: #已经领过了提示
            pass
    except Exception, e:
        logging.exception(e)
        #失败信息
        result = 0

    # return render_to_response('conference/reward.html', locals(), context_instance=RequestContext(request))
    response_data = {}
    response_data['result'] = result
    response_data['data'] = {}
    return HttpResponse(json.dumps(response_data), content_type="application/json")



@csrf_exempt
def conference_survey(request):
    result = 1
    qrcode_url = ''
    # print request.POST
    try:
        ip = get_client_ip(request)
        log_filehandler = open(CONFERENCE_LOG_PATH + '/conference_survey_answers.'
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
        location = request.POST['location']

        conference_survey = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s%s' % \
                         (ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          str(name), srid, identity, telephone, answer1, answer2,
                          answer3, answer4, answer5, answer6, location, '\n')
        # print conference_survey
        # print user_login_log
        log_filehandler.write('%s' % conference_survey)

        # 记录存入数据库
        try:
            survey = Survey()
            survey.srid = srid
            survey.name = name
            survey.identity = identity
            survey.telephone = telephone
            survey.answer1 = answer1
            survey.answer2 = answer2
            survey.answer3 = answer3
            survey.answer4 = answer4
            survey.answer5 = answer5
            survey.answer6 = answer6
            survey.location = location

            survey.save()
        except Exception, e:
            logging.exception(e)

        # 生成二维码
        qrcode_image_url = makeqrimage(survey.id)
        print qrcode_image_url
        result = 1
    except Exception, e:
        logging.exception(e)
        # logging.error(request)
        result = 0
    finally:
        log_filehandler.close()


    response_data = {}
    response_data['result'] = result
    if result == 1:
        response_data['data'] = {'qrcode_url':qrcode_image_url}
    else:
        response_data['data'] = {}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def makeqrimage(sv_id):
    survey = Survey.objects.get(pk=sv_id)

    print "makding qrcode..."
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10,
                   border=4, ) #initialize settings for Output Qrcode
    # qr.add_data(article.download_url) #adds the data to the qr cursor
    # qrcode_url = "http://amway.brixd.com/conference/survey/reward/%s" % sr_no


    qrcode_content_url = "http://a.brixd.com/conference05/gift_confirm.html?id=%d" % (survey.id)
    print qrcode_content_url
    qr.add_data(qrcode_content_url)
    qr.make(fit=True)
    img4qr = qr.make_image()
    qrfilename = "sr_%s" % sv_id
    # # print "\n"
    # file_extension = "jpeg"#10k
    file_extension = "png"#4k
    qrfilename = qrfilename + '.' + file_extension
    filename = rename_file(qrfilename)

    filepath = '%s/conference/' % settings.MEDIA_ROOT
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    image_file = open("%s%s" % (filepath, filename), 'w +') #will open the file, if file does not exist, it will be created and opened.
    img4qr.save(image_file, file_extension.upper()) #write qrcode encoded data to the image file.
    image_file.close() #close the opened file handler.

    print filename
    return filepath.replace(settings.MEDIA_ROOT, DOMAIN + '/media') + filename


def rename_file(filename):
    parts = filename.split(".")
    new_name = time.strftime('%Y%m%d%H%M%S')
    new_name += '%d' % random.randint(10000, 99999)
    new_name += '.%s' % parts[-1]

    return new_name