#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import License, DataSource


admin.site.register(License)
admin.site.register(DataSource)

