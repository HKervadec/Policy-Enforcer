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

    def identify_request(self, s_request):
        return 'POST /v2/meters/' in s_request[0]

    def decide_fate(self, s_request):
        token = extract_token(s_request)
        self.last_token = token

        self.last_request = time()

        if not token in self.token_buffer:
            self.token_buffer[token] = deque(maxlen=self.post_per_min)
            return ""

        if not self.evaluate_buffer(self.token_buffer[token]):
            return "Pushing samples too fast."

        return ""

    def evaluate_buffer(self, buff):
        """
        Will count how much of the last posts have been made in the last minute

        :param buff: The buffer
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

        If the post was successful, will update the last post time.

        :param response: The response
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