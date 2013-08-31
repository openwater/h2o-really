from django.contrib.gis.db import models
from django_hstore import hstore


class Measurement(models.Model):
    """A measurement at a point in space/time."""
    created_timestamp = models.DateTimeField(auto_now_add=True)
    reference_timestamp = models.DateTimeField(
        verbose_name="Observation date/time",
        null=True, blank=True,
        help_text="When was the sample/measurement taken?"
    )
    location = models.PointField()
    location_reference = models.CharField(
        verbose_name="Location name",
        max_length=200, null=True, blank=True,
        help_text="A friendly/reference name for this site")
    observations = hstore.DictionaryField()

    observer = models.EmailField(
        verbose_name="Email address",
        null=True, blank=True,
        help_text="Your email address - don't worry, we won't share it with "
        "anyone!")
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
