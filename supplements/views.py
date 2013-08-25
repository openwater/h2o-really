from django.views.generic.base import TemplateView

from .models import DataSource


class DataSourcesView(TemplateView):
    template_name = "data_sources.html"

    def get_context_data(self, **kwargs):
        context = super(DataSourcesView, self).get_context_data(**kwargs)
        context['datasources'] = DataSource.objects.all()
        return context
