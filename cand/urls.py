from django.contrib import admin
from django.urls import path, include
from apps.accounts.views import home_view
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('', home_view, name='home'),
    path('jobs/', include('apps.jobs.urls')),
    path('applications/', include('apps.applications.urls', namespace='applications')),
    path('messaging/', include('apps.messaging.urls')),  # ✅ seul chemin nécessaire
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
