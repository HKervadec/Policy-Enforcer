#!/usr/bin/env python


class BasePolicy():
    def __init__(self):
        self.apply_policy = False

    def test_request(self, s_request):
        """
        Test a request

        :param s_request: [str*] The request, as an array of strings
        :return: "" is pass the test, a string with explanation otherwise
        :rtype: str
        """
        if not self.identify_request(s_request):
            return ""

        self.apply_policy = True

        return self.decide_fate(s_request)

    def identify_request(self, s_request):
        """
        Find out if the request is managed by this policy.

        :param s_request: [str*] The request, as an array of strings
        :return: True if this policy manage it, False otherwise
        :rtype: bool
        """
        raise NotImplementedError

    def decide_fate(self, s_request):
        """
        Decide the fate of the request.

        :param s_request: [str*] The request, as an array of strings
        :return: "" is will be send to the API, a string with explanation otherwise
        :rtype: str
        """
        raise NotImplementedError

    def analyze_response(self, response):
        """
        Will call the test_response method if self.apply_policy is true.
        Otherwise, do nothing.

        :param response: str The response
        """
        if self.apply_policy:
            self.test_response(response)
            self.apply_policy = False

    def test_response(self, response):
        """
        Test the response. Used mainly for internal purposes.

        :param response: str The response
        """
        raise NotImplementedError