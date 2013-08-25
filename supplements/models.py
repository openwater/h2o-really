from django.db import models


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
