from datetime import timedelta, date
import django_filters

from datetimewidget.widgets import DateTimeWidget
from chosen.widgets import ChosenSelectMultiple

from .models import Measurement, Parameter


class MeasurementFilter(django_filters.FilterSet):
    from_date = django_filters.DateTimeFilter(
        name='reference_timestamp', lookup_type='gte',
        initial=date.today() - timedelta(days=365),
        widget=DateTimeWidget(options={
                'format': 'yyyy/mm/dd',
                'autoclose': 'true',
                'showMeridian': 'true',
                'weekStart': 1,
                'endDate': date.today(),
                'todayBtn': 'true',
                'todayHighlight': 'true',
                'minView': 2,
                'startView': 3,
                'pickerPosition': 'bottom-left',
            })
    )
    to_date = django_filters.DateTimeFilter(
        name='reference_timestamp', lookup_type='lte',
        initial=date.today(),
        widget=DateTimeWidget(options={
                'format': 'yyyy/mm/dd',
                'autoclose': 'true',
                'showMeridian': 'true',
                'weekStart': 1,
                'endDate': date.today() + timedelta(days=1),
                'todayBtn': 'true',
                'todayHighlight': 'true',
                'minView': 2,
                'startView': 3,
                'pickerPosition': 'bottom-left',
            })
    )
    parameter = django_filters.ModelMultipleChoiceFilter(
        label='Parameters',
        name='parameters__parameter', lookup_type='in',
        queryset=Parameter.objects.all(),
        widget=ChosenSelectMultiple,
    )

    class Meta:
        model = Measurement
        fields = ['from_date', 'to_date']

    def __init__(self, *args, **kwargs):
        super(MeasurementFilter, self).__init__(*args, **kwargs)
        self.filters['parameter'].field.help_text = ""
