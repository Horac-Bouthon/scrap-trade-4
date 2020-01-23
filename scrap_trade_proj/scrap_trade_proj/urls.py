from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n'), name='set_language'),
    path('admin/', admin.site.urls),

    path('', include('project_main.urls')),
    path('customers/', include('customers.urls')),
    path('ac_ho/', include('auction_house.urls')),
    path('api/', include('project_api.urls')),
    path('integ/', include('integ.urls')),
    path('doc_repo/', include('doc_repo.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [ path('__debug__/', include(debug_toolbar.urls)) ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
