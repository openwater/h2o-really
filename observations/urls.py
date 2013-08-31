#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import MapView, AddView


urlpatterns = patterns(
    '',
    url(r'^map/', MapView.as_view(), name='observations-map'),
    url(r'^add/', AddView.as_view(), name='observations-add'),
)
