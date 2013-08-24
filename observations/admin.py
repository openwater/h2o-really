#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.gis import admin
from .models import Measurement


admin.site.register(Measurement, admin.GeoModelAdmin)
