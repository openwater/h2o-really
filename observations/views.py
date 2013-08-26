# Create your views here.
from django.views.generic.base import TemplateView

from .models import Measurement


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['measurements'] = Measurement.objects.order_by(
            '-created_timestamp')[:5000]
        return context
