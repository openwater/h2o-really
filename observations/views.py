from django.conf import settings
from django.views.generic.base import TemplateView

from .models import Measurement
from .filters import MeasurementFilter


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(API_KEY=settings.CLOUDMADE_API_KEY)
        f = MeasurementFilter(
            self.request.GET,
            queryset=Measurement.observations_manager.all(),
        )
        context.update({'filter': f})
        return context
