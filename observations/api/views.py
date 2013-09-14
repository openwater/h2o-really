import requests

from rest_framework import generics

from django.conf import settings

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

    def get(self, request, *args, **kwargs):
        """Try and get a response from the java api, fall back to python."""
        try:
            result = requests.get(
                settings.JAVA_API_URL,
                params=request.QUERY_PARAMS.dict()
            )
            if result.status_code == 200:
                return HttpResponse(
                    result.content, mimetype='application/json')
        except Exception, e:
            pass
        return super(MeasurementList, self).get(request, *args, **kwargs)
