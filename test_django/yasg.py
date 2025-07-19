from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class SwaggerApiDoc(TemplateView):
    """Документація API"""
    template_name = 'swagger/swagger_ui.html'
    extra_context = {
        'schema_url': 'openapi-schema'
    }


schema_view = get_schema_view(
    openapi.Info(
        title='Главный переїзд в Німеччину',
        default_version='v 0.0.1',
        description='Документація по API MyRedit',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='mygmail@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [

    path("swagger-ui/", SwaggerApiDoc.as_view(), name="swagger-ui"),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=1), name='schema-json'),

]

