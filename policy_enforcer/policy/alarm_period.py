#!/usr/bin/env python

import re

from base_policy import BasePolicy

from common import identify_create_alarm


class AlarmPeriod(BasePolicy):
    def __init__(self, max_period):
        BasePolicy.__init__(self)

        self.max_period = max_period

    def identify_request(self, a_request):
        return identify_create_alarm(a_request)

    def decide_fate(self, a_request):
        """
        If the period > self.max_period, return False
        """
        period = re.match('.*"period": (\d+)\}.*', a_request[-1])

        if not period:
            return True

        return int(period.group(1)) <= self.max_period

    def gen_error_message(self):
        return "Alarm period is too damn long. Max: %ds" % self.max_period

    def test_response(self, response):
        pass