#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Measurement, TestValue, Test


class TestValueInline(admin.TabularInline):
    model=TestValue

admin.site.register(Measurement, LeafletGeoAdmin, inlines=(TestValueInline,))
admin.site.register(Test)
admin.site.register(TestValue)
