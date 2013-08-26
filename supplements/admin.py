#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.gis import admin as gadmin
from .models import License, DataSource, DataLayer


admin.site.register(License)
admin.site.register(DataSource)
gadmin.site.register(DataLayer, gadmin.GeoModelAdmin)

