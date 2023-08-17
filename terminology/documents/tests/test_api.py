from django.conf import settings

from unittest import TestCase

from django.http import HttpRequest, JsonResponse

from documents.views import get_refbooks, get_elements, check_element

#settings.configure()

class ApiTest(TestCase):
    # def test_get_refbooks(self):
    #     result = get_refbooks()
    #     self.assertEqual()
    #
    # def test_get_elements(self):
    #     result = get_elements()
    #     self.assertEqual()

    def test_check_element(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/1/check_element/'
        request.GET['code'] = 'S08'
        request.GET['value'] = '12345'
        request.GET['version'] = '1'
        result = check_element(request, 1)
        expected_result = JsonResponse('Element found', status=200, safe=False)
        self.assertEqual(expected_result.content, result.content)
