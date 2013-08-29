#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import MapView


urlpatterns = patterns(
    '',
    url(r'^map/', MapView.as_view(), name='observations-map'),
)
