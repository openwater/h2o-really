from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.shortcuts import render

from .models import Measurement
from .forms import MeasurementsForm, ParamRowForm
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


class AddView(View):
    form_class = MeasurementsForm
    initial = {}
    template_name = 'observations.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class ParamRowView(View):
    form_class = ParamRowForm
    initial = {}
    template_name = 'param-row.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial=self.initial, row_id=request.GET.get('nextrow'))
        return render(request, self.template_name, {'form': form})

