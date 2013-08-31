#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, timedelta

import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from datetimewidget.widgets import DateTimeWidget

from .models import Measurement


class PointWidget(forms.gis.PointWidget, forms.gis.BaseGMapWidget):
    pass


class MeasurementsForm(forms.ModelForm):
    """The main obs form which should corrale the various metrics."""
    class Meta:
        model = Measurement
        widgets = {
            'location': PointWidget(attrs={
                'display_wkt': True,
            }),
            'reference_timestamp': DateTimeWidget(options={
                'format': 'yyyy/mm/dd hh:ii P',
                'autoclose': 'true',
                'showMeridian': 'true',
                'weekStart': 1,
                'endDate': date.today() + timedelta(days=1),
                'todayBtn': 'true',
                'todayHighlight': 'true',
            }),
        }
        exclude = ('source',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Where, when & who',
                'location_reference',
                'location',
                'reference_timestamp',
                'observer',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        super(MeasurementsForm, self).__init__(*args, **kwargs)
