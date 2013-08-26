from rest_framework import generics

from observations.models import Measurement
from observations.api.serializers import MeasurementSerializer


class MeasurementList(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()
