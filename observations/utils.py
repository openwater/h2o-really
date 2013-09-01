#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  django.db import connection

def fetch_parameter_keys():
    """Returns a list of current stored parameters. Should be cached."""
    sql = """select distinct k from (
        select skeys(observations) as k
        from observations_measurement
      ) as dt;
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    return [r[0] for r in cursor.fetchall()]

