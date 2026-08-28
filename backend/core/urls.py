"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import mimetypes

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .health import api_root, health


mimetypes.add_type('image/webp', '.webp')


urlpatterns = [
    path('api/', api_root, name='api-root'),
    path('api/health/', health, name='health'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include('apps.analytics.api.routes')),
    path('api/', include('apps.about.api.routes')),
    path('api/', include('apps.contact.api.routes')),
    path('api/', include('apps.technology.api.routes')),
    path('api/', include('apps.projects.api.routes')),
    path('api/', include('apps.resume.api.routes')),
    path('api/', include('apps.project_images.api.routes')),
    path('api/', include('apps.tech_details.api.routes')),
    path('api/', include('apps.lessons.api.routes')),
    path('api/', include('apps.problem_solution.api.routes')),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
