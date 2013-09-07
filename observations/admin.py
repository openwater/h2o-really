#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.gis import admin
from .models import Measurement, TestValue, Test, Parameter


class TestValueInline(admin.TabularInline):
    model=TestValue

admin.site.register(
    Measurement, admin.GeoModelAdmin,
    inlines=(TestValueInline,),
    list_display=('reference_timestamp', 'location_reference', 'observer',
                  'source', '_observed_as_string'),
    search_fields=('location_reference', 'observer', 'source__title', 'parameters__name'),
)
admin.site.register(Test)
admin.site.register(TestValue)
admin.site.register(Parameter)
