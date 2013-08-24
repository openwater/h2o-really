#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "home.html"
