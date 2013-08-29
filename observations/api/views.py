import django_filters
from rest_framework import generics

from observations.models import Measurement
from observations.api.serializers import MeasurementSerializer


class MeasurementFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        name='reference_timestamp', lookup_type='gte',
    )
    to_date = django_filters.DateFilter(
        name='reference_timestamp', lookup_type='lte',
    )

    class Meta:
        model = Measurement
        fields = ['from_date', 'to_date']


class MeasurementList(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    filter_class = MeasurementFilter
    queryset = Measurement.objects.all()
