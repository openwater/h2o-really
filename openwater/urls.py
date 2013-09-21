from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

admin.autodiscover()

from .views import HomePageView


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^contributing/technical/$',
        TemplateView.as_view(template_name="contributing.html"),
        name='contribute-technical'),
    url(r'^sample-kits/$',
        TemplateView.as_view(template_name="sample-kits.html"),
        name="sample-kits"),
    url(r'^supporting-data/', include('supplements.urls')),
    url(r'^observations/', include('observations.urls')),

    url(r'^api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/observations/', include('observations.api.urls')),
    url(r'^api/v1/geocode_postcode$', 'observations.api.views.geocode_postcode', name="geocode_postcode"),
    url(r'^api/v1/geocode_postcode/(?P<postcode>[a-zA-Z0-9 +]+)$', 'observations.api.views.geocode_postcode', name="geocode_postcode"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('diario.urls', namespace='blog', app_name='diario')),
)
