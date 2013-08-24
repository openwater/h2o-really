#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site


def site(request):
    current_site = get_current_site(request)
    return {
        'site': current_site
    }
