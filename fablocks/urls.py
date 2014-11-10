# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'fablocks.views',
    url(r'^$', 'home', name='home'),
)
