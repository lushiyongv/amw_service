# -*- coding:utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sites.models import Site
from settings import STATIC_ROOT

admin.autodiscover()
admin.site.unregister(Site)
urlpatterns = patterns('',
    url(r'^$', 'amway_service.views.index'),
    url(r'^qyh$', 'qingyinghui_invitation.views.index'),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
    #                                                'show_indexes': True}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT,
                                                   'show_indexes': True}),
    url(r'^myinvitation/$', 'qingyinghui_invitation.views.myinvitation'),
    url(r'^login/$', 'qingyinghui_invitation.views.login'),
    url(r'^qyh_schedule/$', 'qingyinghui_invitation.views.schedule'),
    url(r'^qyh/(\w+).html$', 'qingyinghui_invitation.views.show_qyh_html'),


    url(r'^conference/survey/answers/$', 'amway_service.views.conference_survey'),
    url(r'^conference/survey/reward/$', 'amway_service.views.conference_reward'),

    # Examples:
    # url(r'^$', 'qingyinghui_invitation.views.home', name='home'),
    # url(r'^qingyinghui_invitation/', include('qingyinghui_invitation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^yqk/', include('yaoqingka.urls')),


    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
                                                               'show_indexes': False}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,
                                                                'show_indexes': False}),
)

print 'settings.STATIC_ROOT', STATIC_ROOT