import json

from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers

from observations.models import Measurement


class DictionaryField(serializers.Field):
    def to_native(self, obj):
        # HStore doesn't allow nested dictionaries, so we parse the escaped
        # string values to JSON (assuming that's what they in fact are.
        ret = {
            k: json.loads(v) for k, v in obj.items()
        }
        return ret


class MeasurementSerializer(geo_serializers.GeoFeatureModelSerializer):
    observations = DictionaryField()

    class Meta:
        model = Measurement
        geo_field = 'location'
        fields = (
            'created_timestamp', 'reference_timestamp', 'location',
            'location_reference', 'observations', 'source',
        )
