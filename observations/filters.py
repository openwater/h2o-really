import django_filters

from .models import Measurement

class MeasurementFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        name='reference_timestamp', lookup_type='gte',
    )
    to_date = django_filters.DateFilter(
        name='reference_timestamp', lookup_type='lte',
    )
    observed = django_filters.CharFilter(
        name='observations', lookup_type='contains',
    )

    class Meta:
        model = Measurement
        fields = ['from_date', 'to_date', 'observed']
