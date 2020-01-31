from django.urls import reverse
from django.template.loader import render_to_string


class InlineEdit:
    """
    Sends all data needed for the template to generate forms
    for delete, update and create.
    In combination with client-side scripts, can be used for
    intuitive quick-to-navigate forms instead of making separate
    pages for these 3 actions.
    """

    def __init__(self, **KW):
        # Data universal for all entries
        self.heading = KW['heading']
        self.owner = KW['owner']
        self.empty_form = KW['form']()
        self.url_create = reverse(KW['create'], kwargs={'pk': self.owner.pk})

        # Individual entry data
        self.entries = []
        for entry in KW['set']():
            if 'documents' in KW:
                url_docs = reverse(KW['documents'], kwargs={'oid': str(entry.open_id.int_id)})
            else:
                url_docs = ""
            entry_context = {
                'data': entry,
                'filled_form': KW['form'](instance=entry),
                'url_delete': reverse(KW['delete'],
                                      kwargs={'pk': entry.pk}),
                'url_update': reverse(KW['update'],
                                      kwargs={'pk': KW['owner'].pk,
                                              'pk2': entry.pk}),
                'url_docs': url_docs,
            }
            if 'view_through_template' in KW:
                # The data will go through a template
                template_name = KW['view_through_template']
                rendered_html = render_to_string(template_name, {'data': entry})
                entry_context['data'] = rendered_html
            self.entries.append(entry_context)
