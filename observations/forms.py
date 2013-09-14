#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, timedelta

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Button, Field
from datetimewidget.widgets import DateTimeWidget
from leaflet.forms.widgets import LeafletWidget

from .models import Measurement, Parameter, Test, TestValue


class TestValueForm(forms.ModelForm):

    class Meta:
        model = TestValue


class SelectOrCreateTestForm(forms.ModelForm):
    """For a new Test kit, just the basics - we can fill out details later."""
    test = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Test
        exclude = ('parameter', 'meta')

    def __init__(self, *args, **kwargs):
        try:
            param = kwargs.pop('parameter_name')
            row_id = kwargs.pop('row_id')

            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.disable_csrf = True
            self.helper.layout = Layout(
                Field(
                    'test', id='id_test_{0}'.format(row_id),
                ),
                Div(
                    'name',
                    'description',
                    'vendor_or_authority',
                    'unit',
                    'test_type',
                    css_id='test-form-{0}'.format(row_id),
                    css_class='hide new-test',
                )
            )

            super(SelectOrCreateTestForm, self).__init__(*args, **kwargs)
            self.fields['test'].choices = [('', 'Select one')] + [
                (t.id, str(t)) for t in Test.objects.filter(
                    parameter__name=param)
            ] + [('__NEW__', 'Add new...')]
        except KeyError:
            # this is not a select, it must be a create call.
            super(SelectOrCreateTestForm, self).__init__(*args, **kwargs)
            self.fields['test'].choices = [('__NEW__', 'Add new...')]


class ParamRowForm(forms.Form):
    """Just a single obs row."""
    obs_parameter = forms.ChoiceField(
        choices=[],
        label='Parameter',
    )
    new_parameter = forms.CharField(
        label="New parameter name",
        required=False
    )
    measurement = forms.IntegerField()
    value = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        row_id = kwargs.pop('row_id')
        self.helper.layout = Layout(Div(
            Div(
                HTML("<h5>Basics</h5>"),
                Field(
                    'measurement',
                    id='id_measurements_{0}'.format(row_id),
                    type='hidden'
                ),
                Field(
                    'obs_parameter',
                    id='id_obs_parameter_{0}'.format(row_id)
                ),
                Div(
                    FieldWithButtons(
                        Field(
                            'new_parameter',
                            id='id_new_parameter_{0}'.format(row_id)
                        ),
                        StrictButton(
                            "Add",
                            onclick=(
                                "commitNewParam("
                                "'#id_new_parameter_{0}',"
                                "{0},"
                                "'#kit-form-{0} div.kit-container')".format(
                                    row_id))
                        ),
                    ),
                    css_class='hide new-parameter'
                ),
                Field('value', id='id_value_{0}'.format(row_id)),
                css_class='param-row span6',
                css_id='param-form-{0}'.format(row_id)
            ),
            Div(
                HTML("<h5>Test specifics</h5>"),
                Div(css_class='kit-container'),
                css_class='kit-row span6',
                css_id='kit-form-{0}'.format(row_id),
            ),
            css_class='row-fluid',
            css_id='test-value-row-{0}'.format(row_id),
        ))
        super(ParamRowForm, self).__init__(*args, **kwargs)
        self.fields['obs_parameter'].choices = [('', 'Select one')] + [
            (p, p) for p in Parameter.objects.all().values_list(
                'name', flat=True)
        ] + [('__NEW__', 'Add new...')]


class MeasurementsForm(forms.ModelForm):
    """The main obs form which should corrale the various metrics."""
    class Meta:
        model = Measurement
        widgets = {
            'location': LeafletWidget(),
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
        exclude = ('source', 'observations', 'parameters')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_id = "add-observations-form"
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Where, when & who',
                'location_reference',
                'location',
                'reference_timestamp',
                'observer',
                css_id='obs-basics',
            ),
            Fieldset(
                'Observed indicators',
                HTML("<p>Great! Now we know where and when you made the "
                     "observations, we need to know what you found out.</p>"
                     "<p>Below, choose the type of measurement you made (the"
                     " '<strong>parameter</strong>') and how you made the "
                     "measurement (the '<strong>test</strong>').</p>"
                     "<p>If a parameter or test is missing, you can add it "
                     "too. We may follow up to get some more details about the"
                     " test used, since there are so many available.</p>"),
                css_id='param-rows',
                css_class='hide',
            ),
            FormActions(
                StrictButton(
                    'Next', css_class="btn-success",
                    css_id='to-part-2-btn', onclick='commitMeasurement()',
                ),
                Button(
                    'another', 'Add another parameter',
                    css_id='add-another-btn', data_nextrow='1',
                    onclick='addObsRow();',
                    css_class='hide'
                ),
                StrictButton(
                    'Done', css_class='btn-success hide',
                    css_id='finish-btn',
                    onclick='finishUp();'
                ),
            )
        )
        super(MeasurementsForm, self).__init__(*args, **kwargs)
