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