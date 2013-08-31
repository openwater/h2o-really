from rest_framework import generics

from observations.models import Measurement
from observations.api.serializers import (
    CompactMeasurementSerializer, MeasurementSerializer,
)


class MeasurementList(generics.ListAPIView):
    queryset = Measurement.objects.all()

    def get_serializer_class(self):
        if self.request.QUERY_PARAMS.get('compact'):
            return CompactMeasurementSerializer
        else:
            return MeasurementSerializer
