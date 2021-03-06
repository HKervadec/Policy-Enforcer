#!/usr/bin/env python

from time import time
from collections import deque

from base_policy import BasePolicy
from common import extract_token


class SampleRate(BasePolicy):
    def __init__(self, post_per_minute):
        BasePolicy.__init__(self)

        self.last_token = ""
        self.last_request = 0

        self.token_buffer = {}

        self.post_per_min = post_per_minute

    def identify_request(self, a_request):
        return 'POST /v2/meters/' in a_request[0]

    def decide_fate(self, a_request):
        """
        Reject if too much successful post last minute.

        :param a_request:
        :return:
        """
        token = extract_token(a_request)
        self.last_token = token

        self.last_request = time()

        if not token in self.token_buffer:
            self.token_buffer[token] = deque(maxlen=self.post_per_min)
            return True

        return self.evaluate_buffer(self.token_buffer[token])

    def gen_error_message(self):
        return "Pushing samples too fast. Max: %d per minute." % self.post_per_min

    def evaluate_buffer(self, buff):
        """
        Will count how much of the last posts have been made in the last minute

        :param buff: deque(maxlen=self.post_per_min) The buffer
        :return: True if less than the max post per minute, false otherwise
        :rtype: bool
        """
        count = 0
        now = time()

        for date in buff:
            if now - date < 60:
                count += 1

        return count < self.post_per_min

    def test_response(self, response):
        """
        Will test the response.

        If the post was successful, will append the last post time into the token_buffer.

        :param response: str The response
        """
        if self.success_post(response):
            self.token_buffer[self.last_token].append(self.last_request)

    @staticmethod
    def success_post(response):
        """
        Test if the post is successful.

        :param response: str The response
        """
        return '"error_message"' not in response