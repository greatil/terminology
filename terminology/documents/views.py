from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from documents.models import Catalog
from documents.serializers import CatalogsSerializer


#возможно пригодится для гет запроса
from django.http import JsonResponse


def get_refbooks(request):
    date = request.GET.get('startDate')  # Получаем значение параметра date из URL-запроса
    if date:
        catalogs = Catalog.objects.filter(startDate__lte=date)  # Фильтруем справочники по дате начала действия
    else:
        catalogs = Catalog.objects.all()
    data = []  # Создаем список для хранения данных о справочниках

    for catalog in catalogs:
        catalog_data = {
            'id': catalog.id,
            'code': catalog.code,
            'name': catalog.name,
            'catalog_versions': catalog.catalog_versions
        }
        data.append(catalog_data)  # Добавляем данные о справочнике в список
    response = {
        'refbooks': data
    }
    return JsonResponse(response)  # Возвращаем данные в формате JSON


class CatalogViewSet(ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogsSerializer

    # @action(detail=False, methods=['get'])
    # def refbooks(self, request):
    #    date = self.request.query_params.get('date')
    #    if date:
    #        queryset = Catalog.objects.filter(catalogversion__startDate__lte=date).distinct()
    #    else:
    #        queryset = Catalog.objects.all()
    #
    #    serializer = self.get_serializer(queryset, many=True)
    #    return Response({"refbooks": serializer.data})


# class RefbooksListView(generics.ListAPIView):
#     serializer_class = CatalogsSerializer
#
#     def get_queryset(self):
#         date = self.request.query_params.get('date')
#         if date:
#             return Catalog.objects.filter(catalogversion__startDate__lte=date).distinct('id')
#         else:
#             return Catalog.objects.all()
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"refbooks": serializer.data})
