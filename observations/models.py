from django.contrib.gis.db import models
from django_hstore import hstore


class Measurement(models.Model):
    """A measurement at a point in space/time."""
    created_timestamp = models.DateTimeField(auto_now_add=True)
    reference_timestamp = models.DateTimeField(null=True, blank=True)
    location = models.PointField()
    observations = hstore.DictionaryField()

    observer = models.EmailField()

    objects = models.GeoManager()
    observations_manager = hstore.HStoreManager()

    def __unicode__(self):
        return u"Observation at {0}".format(self.created_timestamp)
