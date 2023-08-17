from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from documents.models import Catalog, CatalogElement, CatalogVersion
from documents.serializers import CatalogsSerializer

from django.http import JsonResponse


def get_refbooks(request):
    try:
        input_date_str = request.GET.get('date')
        input_date = datetime.strptime(input_date_str, '%Y-%m-%d').date()
    except Exception as e:
        return JsonResponse({'error': 'Invalid date parameter'}, status=400)

    catalogs = Catalog.objects.filter(catalogversion__startDate__lte=input_date)

    data = []

    for catalog in catalogs:
        catalog_data = {
            'id': catalog.id,
            'code': catalog.code,
            'name': catalog.name
        }
        data.append(catalog_data)
    response = {
        'refbooks': data
    }
    return JsonResponse(response)


def get_elements(request, id):
    try:
        version = request.GET.get('version')
        if version:
            elements = CatalogElement.objects.filter(catalogVersionID=id, catalogVersionID_id__version=version)
        else:
            elements = CatalogElement.objects.filter(catalogVersionID=id,
                                                     catalogVersionID_id__version=CatalogVersion.objects.filter(
                                                         catalogID_id=id).latest('startDate').version)

        data = []
        for element in elements:
            element_data = {
                'code': element.elementCode,
                'value': element.elementValue
            }
            data.append(element_data)

        response = {
            'elements': data
        }
        return JsonResponse(response)
    except Catalog.DoesNotExist:
        return JsonResponse({'error': 'Catalog does not exist'}, status=404)
    except CatalogVersion.DoesNotExist:
        return JsonResponse({'error': 'Catalog version does not exist'}, status=404)


def check_element(request, id):
    code = request.GET.get('code')
    value = request.GET.get('value')
    version = request.GET.get('version')

    if version:
        if (CatalogElement.objects.filter(catalogVersionID=id,
                                          catalogVersionID_id__version=version).first().elementCode ==
            code) and (CatalogElement.objects.filter(catalogVersionID=id,
                                                     catalogVersionID_id__version=version).first().elementValue ==
                       value):
            response = 'Element found'
        else:
            response = 'Element not found'

        return JsonResponse(response, safe=False)
    else:
        if (CatalogElement.objects.filter(catalogVersionID=id,
                                          catalogVersionID_id__version=CatalogVersion.objects.filter(
                                              catalogID_id=id).latest(
                                              'startDate').version).first().elementCode ==
            code) and (CatalogElement.objects.filter(catalogVersionID=id,
                                                     catalogVersionID_id__version=CatalogVersion.objects.filter(
                                                         catalogID_id=id).latest(
                                                         'startDate').version).first().elementValue == value):
            response = 'Element found'
        else:
            response = 'Element not found'

        return JsonResponse(response, safe=False)


class CatalogViewSet(ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogsSerializer
