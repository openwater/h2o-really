# -*- coding: utf-8 -*-
import json
import os
from optparse import make_option
import csv
from datetime import datetime
from logging import getLogger

from django.core.management import BaseCommand, CommandError

import osgb

from observations.models import Measurement, Parameter, Test, TestValue
from supplements.models import DataSource, License

log = getLogger(__name__)

NITRATES = {
    '1': json.dumps({
        'max': '5',
        'min': '0',
        'description': 'Very low',
    }),
    '2': json.dumps({
        'max': '10',
        'min': '5',
        'description': 'Low',
    }),
    '3': json.dumps({
        'max': '20',
        'min': '10',
        'description': 'Moderately low',
    }),
    '4': json.dumps({
        'max': '30',
        'min': '20',
        'description': 'Moderate',
    }),
    '5': json.dumps({
        'max': '40',
        'min': '30',
        'description': 'High',
    }),
    '6': json.dumps({
        'min': '30',
        'description': 'Very high',
    })
}

PHOSPHATES = {
    '1': json.dumps({
        'max': '0.02',
        'min': '0',
        'description': 'Very low',
    }),
    '2': json.dumps({
        'max': '0.06',
        'min': '0.02',
        'description': 'Low',
    }),
    '3': json.dumps({
        'max': '0.1',
        'min': '0.06',
        'description': 'Moderately low',
    }),
    '4': json.dumps({
        'max': '0.2',
        'min': '0.1',
        'description': 'Moderate',
    }),
    '5': json.dumps({
        'max': '1.0',
        'min': '0.2',
        'description': 'High',
    }),
    '6': json.dumps({
        'min': '1.0',
        'description': 'Very high',
    })
}


class Command(BaseCommand):
    help = 'Add data from GQAHI'

    option_list = BaseCommand.option_list + (
        make_option('-n', '--nutrient'),
    )

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError("Specify input filename.")

        if not kwargs['nutrient']:
            raise CommandError("Specify nutrient type. Valid values: N, P")

        self.add_tests()
        with open(args[0], "r") as infile:
            reader = csv.DictReader(infile)
            source, created = DataSource.objects.get_or_create(
                title=os.path.basename(infile.name).split('.')[0],
                attribution='Environment Agency',
                year=2013,
                license=License.objects.get(name='OGL')
            )
            for row in reader:
                self.prepare_row(row, kwargs['nutrient'], source)

    def add_tests(self):
        """Ensure the tests are present in the Test objs."""
        nitrates, created = Parameter.objects.get_or_create(name='Nitrates')
        orthophosphates, created = Parameter.objects.get_or_create(
            name='Orthophosphates')
        self.ea_gqa_nitrates, created = Test.objects.get_or_create(
            parameter=nitrates,
            name="GQA HI Nitrates",
            description="UK Environment Agency GQA HI Nutrients - Nitrates.",
            vendor_or_authority="Environment Agency, UK",
            unit="mg NO3/L",
            meta=NITRATES,
            test_type='CATEGORY'
        )
        self.ea_gqa_orthophates, created = Test.objects.get_or_create(
            parameter=orthophosphates,
            name="GQA HI Orthophosphates",
            description="UK Environment Agency GQA HI Nutrients - Orthophosphates.",
            vendor_or_authority="Environment Agency, UK",
            unit="mg P/L",
            meta=PHOSPHATES,
            test_type='CATEGORY'
        )

    def osgb_to_wgs84(self, ngr):
        lon, lat = osgb.osgb_to_lonlat(ngr)
        return "SRID=4326;POINT({0} {1})".format(lon, lat)

    def prepare_row(self, row, nutrient, source):
        """A CSV row from the GQAHI Nutrients file, as an object"""
        _test = {
            'N': self.ea_gqa_nitrates,
            'P': self.ea_gqa_orthophates,
        }[nutrient]

        for year in [
                1990, 1995, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
                2009]:

            val = row['{0}_GQA_{1}'.format(nutrient[0], str(year)[-2:])]
            if val == '':
                continue
            m = Measurement.objects.create(
                reference_timestamp=datetime(year, 01, 01, 0, 0, 0),
                location=self.osgb_to_wgs84(row['CHEMNGR']),
                location_reference=row['SNAME'],
                source=source,
            )
            TestValue.objects.create(
                measurement=m,
                test=_test,
                value=val
            )
