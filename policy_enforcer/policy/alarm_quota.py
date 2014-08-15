#!/usr/bin/env python

from base_policy import BasePolicy

from common import extract_token, identify_create_alarm


class AlarmQuota(BasePolicy):
    def __init__(self, max_alarm=2):
        BasePolicy.__init__(self)

        self.is_alarm = False
        self.token_memory = {}
        self.last_token = ""

        self.max_alarm = max_alarm

    def identify_request(self, s_request):
        return identify_create_alarm(s_request)

    def decide_fate(self, s_request):
        token = extract_token(s_request)
        self.last_token = token

        if not token in self.token_memory:
            self.token_memory[token] = 0

        return self.token_memory[token] < self.max_alarm

    def gen_error_message(self):
        return "Defined already too much alarms. Max: %d" % self.max_alarm

    def test_response(self, response):
        """
        Will test the response.

        If the alarm creation was a success, it will increment
        the counter for the last token used.

        :param response: The response
        """
        if "HTTP/1.0 201 Created" in response:
            self.token_memory[self.last_token] += 1