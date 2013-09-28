#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def get_value(testvalue):
    """Renders the correct value for the given TestValue."""
    test = testvalue.test
    return test.get_value(testvalue.value)
