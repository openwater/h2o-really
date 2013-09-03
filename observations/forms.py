#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, timedelta

import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Button, Field
from datetimewidget.widgets import DateTimeWidget

from .models import Measurement, Parameter


class PointWidget(forms.gis.PointWidget, forms.gis.BaseGMapWidget):
    pass


def get_new_obs_row(row_id=0):
    """Returns a set of fields that can be used in the measurements form."""
    return Div(
        Field('obs_parameter', id='obs_parameter_{0}'.format(row_id)),
        Field('new_parameter', id='new_parameter_{0}'.format(row_id), type='hidden'),
        Field('xxx', id='xxx_{0}'.format(row_id)),
        HTML('<p>Testing</p>'),
        css_class='obs-row',
        css_id='obs-row-{0}'.format(row_id))


class ParamRowForm(forms.Form):
    """Just a single obs row."""
    obs_parameter = forms.ChoiceField(
        choices=[('', 'Select one')] + [
            (p, p) for p in Parameter.objects.all().values_list(
                'name', flat=True)
        ] + [('__NEW__', 'Add new...')]
    )
    new_parameter = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            get_new_obs_row(kwargs.pop('row_id')),
        )
        super(ParamRowForm, self).__init__(*args, **kwargs)


class MeasurementsForm(forms.ModelForm):
    """The main obs form which should corrale the various metrics."""
    obs_parameter = forms.ChoiceField(
        choices=[('', 'Select one')] + [
            (p, p) for p in Parameter.objects.all().values_list(
                'name', flat=True)
        ] + [('__NEW__', 'Add new...')]
    )
    new_parameter = forms.CharField(required=False)

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
        self.helper.form_id = "add-observations-form"
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            HTML("<h1>This form doesn't work yet!</h1>"),
            HTML("<p>We're still building this bit. Sorry!"),
            Fieldset(
                'Where, when & who',
                'location_reference',
                'location',
                'reference_timestamp',
                'observer',
            ),
            Fieldset(
                'Observed indicators',
                get_new_obs_row(),
                css_id='param-rows',
            ),
            FormActions(
                Button(
                    'another', 'Add another parameter',
                    css_id='add-another-btn', data_nextrow='1',
                    onclick='addObsRow()'),
                Submit(
                    'submit', 'Submit', css_class='button white',
                    onclick='alert("Sorry... we\'re not quite ready yet!")'
                ),
            )
        )
        super(MeasurementsForm, self).__init__(*args, **kwargs)
