from django.contrib import admin
from django.urls import path

from rest_framework import permissions
from documents import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Terminology",
        default_version='v1',
        description="Test description",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('refbooks/', views.get_refbooks, name='get_refbooks'),
    path('refbooks/<int:id>/elements/', views.get_elements, name='get_elements'),
    path('refbooks/<int:id>/check_element/', views.check_element, name='get_elements'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

