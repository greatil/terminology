from unittest import TestCase

from django.http import HttpRequest, JsonResponse

from documents.views import check_element


class CheckElementTestCase(TestCase):

    def test_element_found(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/1/check_element/'
        request.GET['code'] = 'S08'
        request.GET['value'] = '12345'
        request.GET['version'] = '1'
        result = check_element(request, 1)
        expected_result = JsonResponse('Element found', status=200, safe=False)
        self.assertEqual(expected_result.content, result.content)

    def test_element_not_found(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/1/check_element/'
        request.GET['code'] = 'Z13'
        request.GET['value'] = '12'
        request.GET['version'] = '1'
        result = check_element(request, 1)
        expected_result = JsonResponse('Element not found', status=400, safe=False)
        self.assertEqual(expected_result.content, result.content)

    def test_blank_version(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/1/check_element/'
        request.GET['code'] = 'S08'
        request.GET['value'] = '12345'
        request.GET['version'] = ''
        result = check_element(request, 1)
        expected_result = JsonResponse('Element found', status=200, safe=False)
        self.assertEqual(expected_result.content, result.content)

    def test_not_existing_version(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/1/check_element/'
        request.GET['code'] = 'S08'
        request.GET['value'] = '12345'
        request.GET['version'] = '2'
        result = check_element(request, 1)
        expected_result = JsonResponse('Element not found', status=400, safe=False)
        self.assertEqual(expected_result.content, result.content)
