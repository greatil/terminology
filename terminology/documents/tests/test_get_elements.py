import json
from unittest import TestCase

from django.http import HttpRequest

from documents.views import get_elements


class GetElementsTestCase(TestCase):

    def test_correct_input(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/1/elements/'
        request.GET['version'] = '1'
        result = get_elements(request, 1)
        expected_result = json.loads(
            '{"elements": [{"code": "S08", "value": "12345"}, {"code": "S07", "value": "12345"}]}')
        actual_result = json.loads(result.content)
        self.assertEqual(expected_result, actual_result)

    def test_blank_version(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/1/elements/'
        request.GET['version'] = ''
        result = get_elements(request, 1)
        expected_result = json.loads(
            '{"elements": [{"code": "S08", "value": "12345"}, {"code": "S07", "value": "12345"}]}')
        actual_result = json.loads(result.content)
        self.assertEqual(expected_result, actual_result)

    def test_not_existing_version(self):
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/refbooks/1/elements/'
        request.GET['version'] = '3'
        result = get_elements(request, 1)
        expected_result = json.loads(
            '{"elements": []}')
        actual_result = json.loads(result.content)
        self.assertEqual(expected_result, actual_result)
