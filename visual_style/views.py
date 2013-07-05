import os.path
import re

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.base import View, ContextMixin

from .template_finder import find_templates_in_prefix


class VisualStyleView(View, ContextMixin):
    """
    """

    # We can't use a TemplateView because the template rendered
    #  varies based on keyword arguments captured from the URL

    template_prefix = ('visual_style', 'snippets')

    def get_snippets(self, active_template_filename):
        """
        """

        templates = find_templates_in_prefix(*self.template_prefix)
        punctuation_regex = re.compile('[-_]')
        snippets = []

        for template in templates:
            template_filename = os.path.basename(template)
            template_name, _ = os.path.splitext(template_filename)

            snippets.append({
                'url': reverse('style_details', kwargs={
                    'active_template_filename': template_filename
                }),
                'name': re.sub(punctuation_regex, ' ', template_name).title(),
                'is_active': template_filename == active_template_filename,
            })

        return sorted(snippets, key=lambda s: s['name'])

    def get_template_name(self, active_template_filename):
        path_parts = self.template_prefix + (active_template_filename,)
        return os.path.join(*path_parts)

    def get(self, request, active_template_filename=None, *args, **kwargs):
        snippets = self.get_snippets(active_template_filename)
        context = self.get_context_data(**kwargs)
        context['snippets'] = snippets

        if active_template_filename is None and snippets:
            return HttpResponseRedirect(snippets[0]['url'])

        if snippets:
            template_name = self.get_template_name(active_template_filename)
        else:
            template_name = 'visual_style/no_snippets.html'

        return TemplateResponse(
            request=self.request,
            template=template_name,
            context=context,
        )
