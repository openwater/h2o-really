from rest_framework import generics

from observations.filters import MeasurementFilter
from observations.models import Measurement
from observations.api.serializers import (
    CompactMeasurementSerializer, MeasurementSerializer,
)


class MeasurementList(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    filter_class = MeasurementFilter
    queryset = Measurement.observations_manager.all()

    def get_serializer_class(self):
        if self.request.is_ajax() or self.request.QUERY_PARAMS.get('compact'):
            return CompactMeasurementSerializer
        else:
            return MeasurementSerializer
