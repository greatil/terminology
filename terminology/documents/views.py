from datetime import datetime

from documents.models import Catalog, CatalogElement, CatalogVersion

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
    except Catalog.DoesNotExist as exception:
        return JsonResponse({'error': exception}, status=404)
    except CatalogVersion.DoesNotExist as exception:
        return JsonResponse({'error': exception}, status=404)


def check_element(request, id):
    code = request.GET.get('code')
    value = request.GET.get('value')
    version = request.GET.get('version')
    catalog_v_e_table_by_version = CatalogElement.objects.filter(catalogVersionID=id,
                                          catalogVersionID_id__version=version)
    catalog_v_e_table_by_id = CatalogElement.objects.filter(catalogVersionID=id,
                                      catalogVersionID_id__version=CatalogVersion.objects.filter(
                                          catalogID_id=id).latest(
                                          'startDate').version)

    if version:
        if not catalog_v_e_table_by_version:
            return JsonResponse('Element not found', safe=False)

        if (catalog_v_e_table_by_version.first().elementCode == code) \
                and (catalog_v_e_table_by_version.first().elementValue == value):
            return JsonResponse('Element found', safe=False)

        return JsonResponse('Element not found', safe=False)

    if not catalog_v_e_table_by_id:
        return JsonResponse('Element not found', safe=False)

    if (catalog_v_e_table_by_id.first().elementCode == code) \
            and (catalog_v_e_table_by_id.first().elementValue == value):
        return JsonResponse('Element found', safe=False)
    return JsonResponse('Element not found', safe=False)

