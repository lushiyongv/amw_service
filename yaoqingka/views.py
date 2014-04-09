# -*- coding:utf-8 -*-
import string
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.cache import cache
from django.core import serializers

# Create your views here.
from django.template import RequestContext
from common.util.nice_http_util import get_http_referer
from yaoqingka.models import InviteCard
from django.template.defaultfilters import linebreaksbr
import random
from pymongo import Connection
from datetime import datetime

def show_index(request):
    url_referer = get_http_referer(request)
    print url_referer
    if url_referer.find('card') > -1:
        show_animation = False
    else:
        show_animation = True

    normal_card_list = list()
    kwargs = {}
    kwargs['can_show'] = 1
    card_list = get_cards(kwargs)
    # print 'all:', card_list
    for card in card_list:
        normal_card_list.append(card)

    return render_to_response('yaoqingka/index.html', locals(), context_instance=RequestContext(request))

def get_cards(kwargs):
    args_key = '_'.join([str(v) for (k, v) in kwargs.items()])
    # print args_key

    cache_key = 'yaoiqingka_cards_' + args_key
    print cache_key
    cards_in_cache = cache.get(cache_key)
    if cards_in_cache is None:
        cards = InviteCard.objects.filter(**kwargs).order_by("-order", "-id")
        data = serializers.serialize("json", cards)
        cache.set(cache_key, data, 15*60)  # 15分钟
    else:
        cards = []
        card_list_qset = serializers.deserialize("json", cards_in_cache)
        for item in card_list_qset:
            cards.append(item.object)
    # print 'get_cards', args_key, cards
    return cards

def get_card_by_id(card_id):
    cache_key = 'yaoqingka_card_'+card_id
    card_in_cache = cache.get(cache_key)
    if card_in_cache is None:
        try:
            card = InviteCard.objects.get(id=card_id)
        except ObjectDoesNotExist:
            card = None
        cache.set(cache_key, card, 15*60)
    else:
        card = card_in_cache
    return card

def edit_card(request, html_key):
    template_card_id = request.GET.get("id", 0)

    mongoconn = Connection('110.75.189.29', 27017)
    cars_db = mongoconn['yaoqingka']["cards"]
    # print html_key
    item = cars_db.find_one({'_id': html_key})

    # print item
    card = InviteCard()
    card.id = 0
    card.recipient = item['recipient']
    card.content = item['content'].replace('\n', '</br>')
    card.content = item['content'].replace(' ', '&nbsp')
    # print card.content
    card.addressor = item['addressor']
    # print item['card_image']
    image = item['card_image'].replace('http://qstatic.zuimeia.com/img/', '')
    # print image
    card.card_image = image

    card.word_postion = item['word_postion']
    card.word_color = item['word_color']
    card.meeting_time = item['meeting_time']
    card.meeting_location = item['meeting_location']
    card.title = item['title']
    card.id = item['template_card_id']

    card.content = card.content.replace('<p>', '')
    card.content = card.content.replace('</p>', '')
    card.content = card.content.replace('</br>', '\n')
    card.content = card.content.replace('&nbsp', ' ')

    if request.POST:
        print request.POST
        recipient = request.POST.get('recipient')
        content = request.POST.get('content')
        addressor = request.POST.get('addressor')
        card_image = request.POST.get('card_image')
        word_postion = request.POST.get('word_postion')
        meeting_time = request.POST.get('meeting_time')
        meeting_location = request.POST.get('meeting_location')
        word_color = request.POST.get('word_color')
        template_card_id = request.POST.get('template_card_id')
        title = request.POST.get('title')

        # 保存内容生成唯一页面, 存入mongodb
        chars = (string.ascii_letters+string.digits).lower()
        html_key = ''.join(random.sample(chars, 20))
        # print recipient, content, addressor, card_image

        item = {}
        item['_id'] = html_key
        item['recipient'] = recipient
        item['content'] = content
        item['addressor'] = addressor
        item['card_image'] = card_image
        item['word_postion'] = word_postion
        item['meeting_time'] = meeting_time
        item['meeting_location'] = meeting_location
        item['word_color'] = word_color
        item['template_card_id'] = template_card_id
        item['title'] = title

        item['created_at'] = datetime.now()
        cars_db.insert(item)

        # html_key = 'xxxx'
        return HttpResponseRedirect('/yqk/card/show/%s/?id=%d' % (html_key, int(template_card_id)))

    edit_template = False
    return render_to_response('yaoqingka/write_card.html', locals(), context_instance=RequestContext(request))

def edit_template_card(request, template_card_id):
    card = get_card_by_id(template_card_id)
    card.content = card.content.replace('<p>', '')
    card.content = card.content.replace('</p>', '')

    if request.POST:
        print request.POST
        recipient = request.POST.get('recipient')
        content = request.POST.get('content')
        addressor = request.POST.get('addressor')
        card_image = request.POST.get('card_image')
        word_postion = request.POST.get('word_postion')
        meeting_time = request.POST.get('meeting_time')
        meeting_location = request.POST.get('meeting_location')
        word_color = request.POST.get('word_color')
        title = request.POST.get('title')

        chars = (string.ascii_letters+string.digits).lower()
        html_key = ''.join(random.sample(chars, 20))
        # print recipient, content, addressor, card_image

        item = {}
        item['_id'] = html_key
        item['recipient'] = recipient
        item['content'] = content
        item['addressor'] = addressor
        item['card_image'] = card_image

        item['created_at'] = datetime.now()

        item['word_postion'] = word_postion
        item['meeting_time'] = meeting_time
        item['meeting_location'] = meeting_location
        item['word_color'] = word_color
        item['template_card_id'] = template_card_id
        item['title'] = title

        mongoconn = Connection('110.75.189.29', 27017)
        cars_db = mongoconn['yaoqingka']["cards"]
        cars_db.insert(item)

        # html_key = 'xxxx'
        return HttpResponseRedirect('/yqk/card/show/%s/?id=%d' % (html_key, int(template_card_id)))

    edit_template = True
    return render_to_response('yaoqingka/write_card.html', locals(), context_instance=RequestContext(request))

def show_template_card(request):
    url_referer = get_http_referer(request)
    print url_referer
    if url_referer.find('edit') > -1:
        show_weixin = True
    else:
        show_weixin = False
    card = InviteCard()
    addressor = request.GET.get('addressor', None)
    # print addressor
    recipient = request.GET.get('recipient', None)
    content = request.GET.get('content', None)
    card_image = request.GET.get('card_image', None)
    word_postion = request.POST.get('word_postion')
    meeting_time = request.POST.get('meeting_time')
    meeting_location = request.POST.get('meeting_location')
    word_color = request.POST.get('word_color')
    template_card_id = request.POST.get('template_card_id')
    title = request.POST.get('title')
    # card.content = '过去的2013年里，我们一起同舟共济，有过苦、有过累，但此刻再去回想过去的一年的时候，脑海里浮现的满是我们在一起的甜美时光。我好想对你说一声「谢谢」。谢谢你一年来的陪伴和照顾、微笑和阳光。你对我的好是我永远都不会忘记的……'
    card.addressor = addressor
    card.recipient = recipient
    card.content = content
    card.card_image = card_image
    card.word_postion = word_postion
    card.meeting_time = meeting_time
    card.meeting_location = meeting_location
    card.word_color = word_color
    card.id = template_card_id
    card.title = title
    return render_to_response('yaoqingka/display_card.html', locals(), context_instance=RequestContext(request))


def show_card(request, html_key):
    url_referer = get_http_referer(request)

    # if request.COOKIES.has_key('weibojs_70401495'):
    #     show_weibo = True
    # else:
    #     show_weibo =False

    # print url_referer
    if url_referer.find('edit') > -1:
        show_weixin = True
    else:
        show_weixin = False

    mongoconn = Connection('110.75.189.29', 27017)
    cars_db = mongoconn['yaoqingka']["cards"]
    # print html_key
    item = cars_db.find_one({'_id':html_key})

    # print item
    card = InviteCard()
    card.id = 0
    card.recipient = item['recipient']
    card.content = item['content'].replace('\n', '</br>')
    card.content = item['content'].replace(' ', '&nbsp')
    # print card.content
    card.addressor = item['addressor']
    # print item['card_image']
    image = item['card_image'].replace('http://qstatic.zuimeia.com/img/', '')
    # print image
    card.card_image = image

    card.word_postion = item['word_postion']
    card.meeting_time = item['meeting_time']
    card.meeting_location = item['meeting_location']
    card.word_color = item['word_color']
    card.id = item['template_card_id']
    card.title = item['title']

    return render_to_response('yaoqingka/display_card.html', locals(), context_instance=RequestContext(request))