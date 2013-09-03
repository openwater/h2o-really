#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.gis import admin
from .models import Measurement, TestValue, Test


class TestValueInline(admin.TabularInline):
    model=TestValue

admin.site.register(Measurement, admin.GeoModelAdmin, inlines=(TestValueInline,))
admin.site.register(Test)
admin.site.register(TestValue)
