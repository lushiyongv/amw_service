# coding=utf-8
from django.conf.urls import patterns, include, url


urlpatterns = patterns('yaoqingka.views',
    (r'^$', 'show_index'),
    (r'^card/template/(\d+)/edit/$', 'edit_template_card'),
    (r'^card/$', 'show_template_card'),
    (r'^card/show/(\w+)/$', 'show_card'),
    (r'^card/show/(\w+)/edit/$', 'edit_card'),
)