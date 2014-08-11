#!/usr/bin/env python

from base_policy import BasePolicy

from common import extract_token


class QuotaAlarm(BasePolicy):
    def __init__(self):
        self.token_memory = {}
        self.last_token = ""
        self.is_alarm = False

    def test_request(self, s_request):
        """
        Then, test if the token has made < 2 requests since the launch
        of the application

        :param s_request: [str*] The request, as an array of strings
        :return: True if pass the rest, False otherwise
        :rtype: bool
        """
        if not s_request[0] == 'POST /v2/alarms HTTP/1.1':
            return True

        self.is_alarm = True

        token = extract_token(s_request)
        self.last_token = token

        if not token in self.token_memory:
            self.token_memory[token] = 0

        return self.token_memory[token] < 2

    def test_response(self, response):
        """
        Will test the response.
        If the alarm creation was a success, it will increment
        the counter for the last token used.

        :param response: The response
        """
        if self.is_alarm and "HTTP/1.0 201 Created" in response:
            self.token_memory[self.last_token] += 1
            self.is_alarm = False