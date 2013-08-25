#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import DataSourcesView


urlpatterns = patterns(
    '',
    # Examples:
    url(r'sources', DataSourcesView.as_view(), name='supplements-sources'),
)
