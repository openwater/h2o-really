from django.db import models
from django.contrib.gis.db import models as gmodels
from django_hstore import hstore


class License(models.Model):
    """A license under which a DataSource is published and useable."""
    name = models.CharField(max_length=50)
    url = models.URLField(help_text="A link to this license.")
    version = models.CharField(
        max_length=10, blank=True, null=True,
        help_text="If this is some version of the license, identify it.")
    body = models.TextField(
        blank=True, null=True,
        help_text="If there is no URL available, you can paste the license.")

    def __unicode__(self):
        return self.name


class DataSource(models.Model):
    """A data source from a third party."""
    title = models.CharField(max_length=100)
    attribution = models.TextField(
        help_text="The attribution as the author requested it.")
    year = models.PositiveIntegerField()
    license = models.ForeignKey(License)

    def __unicode__(self):
        return self.title


class DataLayer(gmodels.Model):
    """Any external data that has a geometry that can be added to the map."""
    name = gmodels.CharField(max_length=200)
    description = gmodels.TextField(null=True, blank=True)
    added = gmodels.DateTimeField(auto_now_add=True)
    source = gmodels.ForeignKey(DataSource)
    shape = gmodels.GeometryField()
    info = hstore.DictionaryField(
        null=True, blank=True,
        help_text="Any supplementary data for this shape.")
