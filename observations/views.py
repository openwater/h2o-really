import json

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.views.generic import CreateView
from django.shortcuts import render
from django.http import HttpResponse

from .models import Measurement, Parameter
from .forms import MeasurementsForm, ParamRowForm, SelectOrCreateTestForm
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


class AddView(CreateView):
    form_class = MeasurementsForm
    template_name = 'observations.html'

    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data(**kwargs)
        context.update(API_KEY=settings.CLOUDMADE_API_KEY)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            measurement = form.save()
            return HttpResponse(
                json.dumps({'message': 'OK', 'id': measurement.id}))
        else:
            return HttpResponse(json.dumps(form.errors), status=400)


class ParamRowView(View):
    form_class = ParamRowForm
    initial = {}
    template_name = 'param-row.html'

    def get(self, request, *args, **kwargs):
        row_id = request.GET.get('nextrow')
        measurement_id = request.GET.get('measurement')
        initial = dict(self.initial)
        initial.update({'measurement_id': measurement_id})
        form = self.form_class(initial=initial, row_id=row_id)
        return render(
            request, self.template_name, {'form': form, 'row_id': row_id})

    def post(self, request, *args, **kwargs):
        try:
            p = Parameter.objects.get(name__iexact=request.POST.get('name'))
            # correct the user's input
            return HttpResponse(
                json.dumps({'message': 'exists', 'name': p.name}),
                mimetype='application/json'
            )
        except Parameter.DoesNotExist:
            Parameter.objects.create(name=request.POST.get('name'))
            return HttpResponse(
                json.dumps({'message': 'ok'}),
                mimetype='application/json'
            )


class TestRowView(View):
    form_class = SelectOrCreateTestForm
    initial = {}
    template_name = 'test-row.html'

    def get(self, request, *args, **kwargs):
        param = request.GET.get('param', False)
        row_id = request.GET.get('row_id', False)
        if not param or not row_id:
            raise  # TODO: be better...
        form = self.form_class(
            initial=self.initial, parameter_name=param, row_id=row_id)
        return render(
            request, self.template_name, {'form': form, 'row_id': row_id})
