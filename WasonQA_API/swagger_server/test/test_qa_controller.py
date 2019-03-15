# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.answer import Answer
from swagger_server.models.question import Question
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestQAController(BaseTestCase):
    """ QAController integration test stubs """

    def test_api_post(self):
        """
        Test case for api_post

        QA
        """
        body = Question()
        response = self.client.open('/openapi/api',
                                    method='POST',
                                    data=json.dumps(body),
                                    content_type='application/json')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
