import json

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.views.generic import CreateView, DetailView
from django.shortcuts import render
from django.http import HttpResponse

from .models import Measurement, Parameter, TestValue
from .forms import MeasurementsForm, ParamRowForm, SelectOrCreateTestForm, TestValueForm
from .filters import MeasurementFilter


class MeasurementView(DetailView):
    template_name = 'observation.html'
    model = Measurement

    def get_context_data(self, **kwargs):
        context = super(MeasurementView, self).get_context_data(**kwargs)
        context.update(API_KEY=settings.CLOUDMADE_API_KEY)
        return context


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
        measurement = request.GET.get('measurement')
        initial = dict(self.initial)
        initial.update({'measurement': measurement})
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

    def post(self, request, *args, **kwargs):
        # fail fast if there is not even a value
        if request.POST.get('value').strip() == '':
            return HttpResponse(json.dumps({
                'value': ["This field is required."]
            }), status=400)
        # fail fast if there is not even a param
        if request.POST.get('obs_parameter').strip() == '':
            return HttpResponse(json.dumps({
                'obs_parameter': ["This field is required."]
            }), status=400)

        # OK, is this a new test or an old one?
        if request.POST.get('test') != '__NEW__':
            _type = 'test-value'
            form_class = TestValueForm
        else:  # old one
            _type = 'test'
            form_class = self.form_class

        form = form_class(request.POST)

        if form.is_valid():
            if _type == 'test-value':
                testvalue = form.save()
            else:
                test = form.save(commit=False)
                test.parameter = Parameter.objects.get(
                    name__iexact=request.POST.get('obs_parameter'))
                test.save()
                # TODO: value validation here, somehow, against test meta.
                testvalue = TestValue.objects.create(
                    test=test,
                    measurement_id=request.POST.get('measurement'),
                    value=request.POST.get('value')
                )
            return render(
                request, 'test-value-row.html', {'testvalue': testvalue})
        else:
            return HttpResponse(json.dumps(form.errors), status=400)
