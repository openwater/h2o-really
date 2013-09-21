import os
import csv
import urllib
import json
import tempfile
import zipfile
import shutil

from StringIO import StringIO

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.views.generic import CreateView, DetailView
from django.shortcuts import render
from django.http import HttpResponse

#from shapes.views import ShpResponder
import shapefile

from unidecode import unidecode

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


class ReportView(TemplateView):
    template_name = 'report.html'


class DownloadView(View):

    def _write_response(self, queryset, params, shp=None, csv_writer=None):
        """Write CSV or SHP."""
        for obj in queryset.defer('observations').select_related('parameters'):
            testvalues = obj.testvalue_set
            if params:  # we only want the params we asked for
                # TODO: I don't really like this.
                testvalues = testvalues.filter(test__parameter__id__in=params)
            else:
                testvalues = testvalues.all()
            for testvalue in testvalues:
                if shp:
                    shp.point(obj.location.x, obj.location.y)
                    shp.record(
                        obj.created_timestamp,
                        obj.reference_timestamp,
                        unidecode(obj.location_reference),
                        testvalue.test.parameter.name,
                        testvalue.value,
                        str(testvalue.test)
                    )
                if csv_writer:
                    csv_writer.writerow([
                        obj.location.x, obj.location.y,
                        obj.created_timestamp,
                        obj.reference_timestamp,
                        unidecode(obj.location_reference),
                        testvalue.test.parameter.name,
                        testvalue.value,
                        str(testvalue.test)]
                    )

    def shp_zip_response(self, queryset, params):
        """Render a shapefile(s), and zip it up, send it back in Response."""
        mimetype = 'application/zip'
        shp = shapefile.Writer(shapefile.POINT)

        shp.field('DT_created', 'C', '32')
        shp.field('DT_reference', 'C', '32')
        shp.field('location_name', 'C', '200')
        shp.field('parameter', 'C', '100')
        shp.field('value', 'C', '100')
        shp.field('test', 'C', '100')

        self._write_response(queryset, params, shp=shp)

        tmp = tempfile.mkdtemp()
        name = 'observations'
        path = os.path.join(tmp, name)
        shp.save(path)
        prj = urllib.urlopen(
            "http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(
                '4326'))
        prj_fp = open(".".join((os.path.join(tmp, name), 'prj')), 'w')
        prj_fp.write(prj.read())
        prj_fp.close()

        # make the zip
        buffer = StringIO()
        zip = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)
        files = ['shp', 'shx', 'prj', 'dbf']
        for item in files:
            filename = '{0}.{1}'.format(path, item)
            if os.path.exists(filename):
                zip.write(filename, arcname='{0}.{1}'.format(name, item))
        zip.close()
        buffer.flush()
        zip_stream = buffer.getvalue()
        buffer.close()

        # make the response
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename={0}.zip'.format(
            name)
        response['Content-length'] = str(len(zip_stream))
        response['Content-Type'] = mimetype
        response.write(zip_stream)

        shutil.rmtree(tmp)
        return response

    def csv_response(self, queryset, params):
        """Return a CSV response."""
        name = 'observations'
        mimetype = 'text/csv'
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(
            name)
        response['Content-Type'] = mimetype
        csv_writer = csv.writer(response)
        csv_writer.writerow([
            'longitude',
            'latitude',
            'datetime_created',
            'datetime_reference',
            'location_name',
            'parameter',
            'value',
            'test',
        ])

        self._write_response(queryset, params, csv_writer=csv_writer)
        return response

    def get(self, request, *args, **kwargs):
        f = MeasurementFilter(
            self.request.GET,
            queryset=Measurement.observations_manager.all(),
        )
        return {
            'csv': self.csv_response,
            'shp': self.shp_zip_response,
        }[request.GET.get('format', 'csv')](f.qs, f.data.get('parameter', []))


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
