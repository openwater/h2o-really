from django.conf.urls import url
from django.conf.urls import patterns

from rest_framework.urlpatterns import format_suffix_patterns

from observations.api.views import MeasurementList


urlpatterns = patterns(
    '',
    url(r'^measurements/$', MeasurementList.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
