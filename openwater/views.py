#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView

from diario.models import Entry
from observations.models import Measurement


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['entry_list'] = Entry.objects.all()[:3]
        context['measurement_list'] = Measurement.objects.order_by('-created_timestamp')[:5]
        return context
