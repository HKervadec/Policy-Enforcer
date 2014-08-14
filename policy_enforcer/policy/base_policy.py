#!/usr/bin/env python


class BasePolicy():
    def __init__(self):
        self.apply_policy = False
        self.error_template = '{"error_message": {"debuginfo": null, "faultcode": "PolicyEnforcer", "faultstring": "%s"}}'

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

        if not self.decide_fate(s_request):
            return self.error_template % self.gen_error_message()

        return ""

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
        :return: True if it will be send to the API, False otherwise.
        :rtype: int
        """
        raise NotImplementedError

    def gen_error_message(self):
        """
        Generate an error message in case of refused request.

        :return: The [customized] error message
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