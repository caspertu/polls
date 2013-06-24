#!/usr/bin/env python
# coding: utf-8
# casper@2013/05/27

from django.conf.urls import patterns, include, url
from django.contrib import admin
from pollapp.views import my_login, my_logout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/', include('pollapp.urls', namespace='polls')),
    
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login$', my_login, name='login'),
    url(r'^logout$', my_logout, name='logout'),
    url(r'^signin$', 'pollapp.views.display_signin_page', name='signin'),
)
