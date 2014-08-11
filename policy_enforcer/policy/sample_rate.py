#!/usr/bin/env python

from time import time

from base_policy import BasePolicy
from common import extract_token


class SampleRate(BasePolicy):
    def __init__(self, post_per_minute):
        BasePolicy.__init__(self)

        self.last_token = ""
        self.last_successful_post = {}

        self.rate = 60. / post_per_minute

    def identify_request(self, s_request):
        return 'POST /v2/meters/' in s_request[0]

    def decide_fate(self, s_request):
        token = extract_token(s_request)
        self.last_token = token

        try:
            delta = time() - self.last_successful_post[token]

            return delta > self.rate
        except KeyError:
            return True

    def test_response(self, response):
        """
        Will test the response.

        If the post was successful, will update the last post time.

        :param response: The response
        """
        if self.success_post(response):
            self.last_successful_post[self.last_token] = time()

    @staticmethod
    def success_post(response):
        """
        Test if the post is successful.

        :param response: str The response
        """
        return '"error_message"' not in response