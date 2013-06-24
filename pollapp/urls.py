#!/usr/bin/env python
# coding: utf-8
# casper@2013/05/27

from django.conf.urls import patterns, url
from pollapp import views

urlpatterns = patterns('',
    # list new create save analysis for poll
    url(r'^create/$',   views.create,       name='create'),
    url(r'^list/$',     views.poll_list,    name='index'),
    url(r'^new/$',      views.poll_new,     name='poll_new'),
    url(r'^save/$',     views.poll_save,    name='poll_save'),
    url(r'^analysis/$', views.poll_analysis,name='poll_analysis'),
    url(r'^(?P<pk>\d+)/$',      views.poll_detail,          name='detail'),

    # for guest
    url(r'^s/(?P<code>\w+)/$',      views.poll_guest_answer,  name='poll_guest_answer'),
    url(r'^(?P<code>\w+)/update$',  views.poll_answer_update, name='poll_answer_update'),

    # 联系人
    url(r'^contact/$',      views.contact,      name='contact'),
     url(r'^contact/(?P<pk>\d+)$',      views.group_detail,      name='group_detail'),
    url(r'^contact/add/$',  views.contact_add,  name='contact_add'),

    # API
    url(r'^contacts/$', views.ContactList.as_view()),
    url(r'^contacts/(?P<pk>[0-9]+)/$', views.ContactDetail.as_view()),
)