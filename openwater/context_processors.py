#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.conf import settings


def site(request):
    current_site = get_current_site(request)
    return {
        'site': current_site
    }

def settings(request):
    return {
        'settings': {
            'CLOUDMADE_API_KEY': settings.CLOUDMADE_API_KEY,
            'MAPIT_URL': settings.MAPIT_URL,
        }
    }