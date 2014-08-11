#!/usr/bin/env python

from time import time

from base_policy import BasePolicy
from common import extract_token


class SampleRate(BasePolicy):
    def __init__(self, post_per_minute):
        self.last_token = ""
        self.last_successful_request = {}

        self.rate = 60. / post_per_minute

    def test_request(self, s_request):
        """
        'POST /v2/meters/policy_test HTTP/1.1\r\nUser-Agent: curl/7.35.0\r\nHost: qos107.research.att.com:8777\r\nAccept: */*\r\nX-Auth-Token: f125a267b5fd4ce4b7adc1f6e9f7efdf\r\nContent-Type: application/json\r\nContent-Length: 410\r\n\r\n[   {          "counter_name": "policy_test",          "user_id": "7c875184eb5d4a42b76f575ee19132a1",          "resource_id": "39a934f9-3f46-410f-b0a3-b469462e78cc",          "resource_metadata": {            "display_name": "Pata Pata"           },          "counter_unit": "%",          "counter_volume": 13.37,          "project_id": "39b219aaa21c4677ae7dee310ddb3790",          "counter_type": "gauge"   }]'
        Test if the token respect the limit rate.

        :param s_request: str The request
        :return: True is pass the test, False otherwise
        :rtype: bool
        """
        token = extract_token(s_request)
        self.last_token = token

        try:
            delta = time() - self.last_successful_request[token]

            return delta > self.rate
        except KeyError:
            return True

    def test_response(self, response):
        if self.success_post(response):
            self.last_successful_request[self.last_token] = time()

    @staticmethod
    def success_post(response):
        return '"error_message"' not in response

