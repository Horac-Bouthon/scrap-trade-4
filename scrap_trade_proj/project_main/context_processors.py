#  
#  Context processors
#  
#  Processor functions take in a `HttpRequest` (same as for `render` in views) 
#  and return a dictionary, which is added to the final context of any page 
#  that uses the context processor. 
#  
#  If these functions are added to `settings.TEMPLATES`, the context
#  processor works globally across all the project's pages.
# 


from .models import Project
def project(request):
    return { 
        'project': Project.objects.first() 
    }
    
