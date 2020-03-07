
from django import template
from django.utils.html import format_html

# `register` variable being here (not the call) tells Django 
# that this file is a file with custom filters and tags.
register = template.Library()  


@register.simple_tag
def icon(my_name):  
    """
    Translate my name of an icon to a variant in the icon set
    that I chose to work with. Allows me to write actual meaning
    behind the icon instead of a piece of text like 'eye'.

    In the future, I can precompile the icon SVG's and translate
    it directly into HTML and not rely on the HTML reformatting
    Javascript call on the frontend. Would save some data and time.
    """
    TO_FEATHER = {  
        # Translation table
        'edit': 'edit-3',
        'add': 'plus',
        'delete': 'trash-2',
        'close': 'x',
        'cancel': 'x',
        'save': 'check',
        
        'ajax_add': 'plus-circle',
        'ajax_save': 'check-circle',
        
        'download': 'download',
        'new_tab': 'external-link',
        'send': 'send',
        'doc': 'file-text',
        
        'previous': 'chevron-left',
        'next': 'chevron-right',
        
        'collapse': 'chevron-down',
        'winner': 'award',
    }
    html = format_html(
        '<i data-feather="{}" data-calledwith="{}"></i>', 
        TO_FEATHER[my_name],
        my_name  # For debugging
    )
    return html 



from django.utils.translation import gettext as _

@register.simple_tag
def button(type, extra_classes, href=None):
    assert False, 'Not implemented'
    
    
