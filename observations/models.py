from django.contrib.gis.db import models
from django_hstore import hstore


class Measurement(models.Model):
    """A measurement at a point in space/time."""
    created_timestamp = models.DateTimeField(auto_now_add=True)
    reference_timestamp = models.DateTimeField(null=True, blank=True)
    location = models.PointField()
    location_reference = models.CharField(
        max_length=200, null=True, blank=True,
        help_text="A friendly/reference name for this site")
    observations = hstore.DictionaryField()

    observer = models.EmailField(
        null=True, blank=True,
        help_text="If a Citizen Scientist added this data - their email.")
    source = models.ForeignKey(
        'supplements.DataSource', null=True, blank=True,
        help_text="If this data came from an historic source, what is it?"
    )

    objects = models.GeoManager()
    observations_manager = hstore.HStoreManager()

    class Meta:
        ordering = ('-reference_timestamp',)

    def __unicode__(self):
        return u"Observation at {0}".format(self.created_timestamp)
