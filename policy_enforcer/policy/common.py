#!/usr/bin/env python

import re


def extract_token(s_request):
    """
    X-Auth-Token: 6a9aac95bf8a49bcac02db661c42c1cd
    Will extract the token of the request.

    :param s_request: [str*] The request, as an array of strings
    :return: The token
    :rtype: str
    """
    for part in s_request:
        grouped = re.match(r"X-Auth-Token: ([a-f\d]+)", part)

        if grouped:
            return grouped.group(1)


def identify_create_alarm(a_request):
    """
    Identify a request to create an alarm.

    :param a_request: [str*] The request, as an array of strings
    :return: True if is one, False otherwise
    :rtype: bool
    """
    return a_request[0] == 'POST /v2/alarms HTTP/1.1'