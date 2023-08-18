import json
from unittest import TestCase

from django.http import HttpRequest, JsonResponse

from documents.views import get_refbooks


class GetRefbooksTestCase(TestCase):

    def test_first_date(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/'
        request.GET['date'] = '2023-08-13'
        result = get_refbooks(request)
        expected_result = json.loads(
            '{"refbooks": [{"id": 1, "code": "123", "name": "321"}]}')
        actual_result = json.loads(result.content)
        self.assertEqual(expected_result, actual_result)

    def test_last_date(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/'
        request.GET['date'] = '2023-08-14'
        result = get_refbooks(request)
        expected_result = json.loads(
            '{"refbooks": [{"id": 1, "code": "123", "name": "321"}, {"id": 1, "code": "123", "name": "321"}]}')
        actual_result = json.loads(result.content)
        self.assertEqual(expected_result, actual_result)

    def test_no_date(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/'
        request.GET['date'] = ''
        result = get_refbooks(request)
        expected_result = json.loads(
            '{"error": "Invalid date parameter"}')
        actual_result = json.loads(result.content)
        self.assertEqual(expected_result, actual_result)

    def test_date_before_first_version(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/'
        request.GET['date'] = '2023-08-12'
        result = get_refbooks(request)
        expected_result = json.loads(
            '{"refbooks": []}')
        actual_result = json.loads(result.content)
        self.assertEqual(expected_result, actual_result)
