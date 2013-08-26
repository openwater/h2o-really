#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys
import argparse
import csv
from datetime import datetime

import osgb

project_root = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../'
))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openwater.settings")

from django.conf import settings

from observations.models import Measurement
from supplements.models import DataSource, License

NITRATES = {
    '1': {
        'max': '5',
        'min': '0',
        'description': 'Very low',
        'unit': 'mg NO3/I',
    },
    '2': {
        'max': '10',
        'min': '5',
        'description': 'Low',
        'unit': 'mg NO3/I',
    },
    '3': {
        'max': '20',
        'min': '10',
        'description': 'Moderately low',
        'unit': 'mg NO3/I',
    },
    '4': {
        'max': '30',
        'min': '20',
        'description': 'Moderate',
        'unit': 'mg NO3/I',
    },
    '5': {
        'max': '40',
        'min': '30',
        'description': 'High',
        'unit': 'mg NO3/I',
    },
    '6': {
        'min': '30',
        'description': 'Very high',
        'unit': 'mg NO3/I',
    }
}

PHOSPHATES = {
    '1': {
        'max': '0.02',
        'min': '0',
        'description': 'Very low',
        'unit': 'mgP/I',
    },
    '2': {
        'max': '0.06',
        'min': '0.02',
        'description': 'Low',
        'unit': 'mgP/I',
    },
    '3': {
        'max': '0.1',
        'min': '0.06',
        'description': 'Moderately low',
        'unit': 'mgP/I',
    },
    '4': {
        'max': '0.2',
        'min': '0.1',
        'description': 'Moderate',
        'unit': 'mgP/I',
    },
    '5': {
        'max': '1.0',
        'min': '0.2',
        'description': 'High',
        'unit': 'mgP/I',
    },
    '6': {
        'min': '1.0',
        'description': 'Very high',
        'unit': 'mgP/I',
    }
}


def osgb_to_wgs84(ngr):
    lon, lat = osgb.osgb_to_lonlat(ngr)
    return "SRID=4326;POINT({0} {1})".format(lon, lat)


def prepare_row(row, nutrient, source):
    """A CSV row from the GQAHI Nutrients file, as an object"""
    _nutrient = {
        'N': NITRATES,
        'P': PHOSPHATES,
    }[nutrient]

    param_name = {
        'N': 'Nitrates',
        'P': 'Orthophosphates',
    }[nutrient]

    measurements = []
    for year in [
            1990, 1995, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
            2009]:

        val = row['{0}_GQA_{1}'.format(nutrient[0], str(year)[-2:])]
        if val == '':
            continue
        measurements.append(
            Measurement(
                reference_timestamp=datetime(year, 01, 01, 0, 0, 0),
                location=osgb_to_wgs84(row['CHEMNGR']),
                location_reference=row['SNAME'],
                source=source,
                observations={
                    param_name: json.dumps(_nutrient[val])
                }

            )
        )
    Measurement.objects.bulk_create(measurements)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add data from GQAHI')
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--nutrient', '-n')
    args = parser.parse_args()
    reader = csv.reader(args.infile)
    header = reader.next()
    source, created = DataSource.objects.get_or_create(
        title=args.infile.name.split('/')[-1].split('.')[0],
        attribution='Environment Agency',
        year=2013,
        license=License.objects.get(name='OGL')
    )
    for row in reader:
        _row = dict(zip(header, row))
        prepare_row(_row, args.nutrient, source)
