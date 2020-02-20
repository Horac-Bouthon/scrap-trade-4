#  
#  Context processors
#  
#  Processor functions take in a `HttpRequest` (same as for `render` in views) 
#  and return a dictionary, which is added to the final context of any page.
#  
#  These functions must be then mentioned in `settings.TEMPLATES`.
# 


from .models import Project
from scrap_trade_proj.settings import DEBUG_OFFLINE

def project(request):
    return { 
        'project': Project.objects.first(), 
        'debug_offline': DEBUG_OFFLINE,
    }
    
