from datetime import timedelta, date
import django_filters

from datetimewidget.widgets import DateTimeWidget

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
            })
    )

    class Meta:
        model = Measurement
        fields = ['from_date', 'to_date', 'parameters']
