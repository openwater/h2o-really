from django.contrib.gis.db import models
from django_hstore import hstore


class Parameter(models.Model):
    """Some parameter of quality that needs monitoring."""
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Test(models.Model):
    """Lays out a load of meta stuff about a particular test.

    The meta field should be used like this:
        Say we have a test like EA GQA, where they have numbered categories
        which correspond to a range of values, but it is not clear what the
        actual value obtained is - in this case, the meta field stores all the
        category IDs and the value stored in the through relationship would be
        the category identifier.

        With a test like La Motte 5982 TesTab Phosphate kit, the meta would
        contain the available colorimetric categories (which correspond to an
        actual PPM value - but only certain colorimetrics are available, rather
        than a continuous scale).

        With a presence/absence test, the meta would contain presence and
        absence categories, perhaps with a note about degree of certainty. The
        value stored in the through relationship would be 'present' or 'absent'

    """
    parameter = models.ForeignKey(Parameter)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    vendor_or_authority = models.CharField(
        max_length=100,
        help_text="The name of the Manufacturer, Vendor, or Authority etc "
        "associated with this test."
    )
    unit = models.CharField(max_length=50)
    meta = hstore.DictionaryField(
        help_text="Describe all the potential values this test can result in."
    )
    test_type = models.CharField(
        max_length=20,
        choices=(
            ('CATEGORY', 'Category'),
            ('VALUE', 'Value'),
            ('TEXT', 'Text'),
            ('PRESENCE', 'Present/Absent')
        )
    )

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.vendor_or_authority)


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
    observations = hstore.DictionaryField(null=True, blank=True)
    parameters = models.ManyToManyField(Test, through='TestValue')

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

    def _observed_as_string(self):
        """Returns a list of parameter names that were obeserved."""
        return ", ".join([
            test.parameter.name for test in self.parameters.all()])


class TestValue(models.Model):
    """A Test, as measured during a Measurement, resulting in a Value."""
    test = models.ForeignKey(Test)
    measurement = models.ForeignKey(Measurement)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return u"{0} in {1}: {2}".format(
            self.test, self.measurement, self.value)
