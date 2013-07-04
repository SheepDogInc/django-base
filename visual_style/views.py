from django.views.generic import TemplateView

from .template_finder import find_templates_in_prefix


class VisualStyleView(TemplateView):
    template_name = 'visual_style/all-styles.html'

    def get_context_data(self, **kwargs):
        context = super(VisualStyleView, self).get_context_data(**kwargs)
        context['partials'] = find_templates_in_prefix('visual_style', 'snippets')
        return context
