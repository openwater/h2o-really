#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (
    MapView, AddView, ParamRowView, TestRowView, MeasurementView,
    DownloadView, ReportView, MeasurementPopupView
)


urlpatterns = patterns(
    '',
    url(r'^map/', MapView.as_view(), name='observations-map'),
    url(r'^report/', ReportView.as_view(), name='observations-report'),
    url(r'^download/', DownloadView.as_view(), name='observations-download'),
    url(r'^detail/(?P<pk>\d+)/$', MeasurementView.as_view(), name='observations-detail'),
    url(r'^detail/(?P<pk>\d+)/popup/$', MeasurementPopupView.as_view(), name='observations-detail-popup'),
    url(r'^add/$', AddView.as_view(), name='observations-add'),
    url(r'^add/param/$', ParamRowView.as_view(), name='observations-add-param'),
    url(r'^add/test/$', TestRowView.as_view(), name='observations-add-test'),
)
