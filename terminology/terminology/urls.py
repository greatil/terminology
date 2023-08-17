from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from documents import views

from documents.views import CatalogViewSet

router = SimpleRouter()

router.register('api/catalogs', CatalogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('refbooks/', views.get_refbooks, name='get_refbooks'),
    path('refbooks/<int:id>/elements/', views.get_elements, name='get_elements'),
    path('refbooks/<int:id>/check_element/', views.check_element, name='get_elements'),
]

urlpatterns += router.urls
