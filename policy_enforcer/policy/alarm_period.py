#!/usr/bin/env python

import re

from base_policy import BasePolicy

from common import identify_create_alarm


class AlarmPeriod(BasePolicy):
    def __init__(self, max_period):
        BasePolicy.__init__(self)

        self.max_period = max_period

    def identify_request(self, s_request):
        return identify_create_alarm(s_request)

    def decide_fate(self, s_request):
        """
        If the period > self.max_period, return False
        """
        period = re.match('.*"period": (\d+)\}.*', s_request[-1])

        if not period:
            return ""

        if not int(period.group(1)) <= self.max_period:
            return "Alarm period is too damn long."

        return ""

    def test_response(self, response):
        pass