#!/usr/bin/env python


class BasePolicy():
    def __init__(self):
        raise NotImplementedError

    def test_request(self, s_request):
        """
        Test a request

        :param s_request: str The request
        :return: True is pass the test, False otherwise
        :rtype: bool
        """
        raise NotImplementedError

    def test_response(self, response):
        """
        Test the response.
        Used mainly for internal purposes

        :param response: str The response
        """
        raise NotImplementedError