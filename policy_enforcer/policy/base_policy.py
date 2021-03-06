#!/usr/bin/env python

from time import asctime, gmtime


class BasePolicy():
    def __init__(self):
        self.apply_policy = False
        self.error_header_template = "HTTP/1.0 403 Forbidden\r\nDate: %s GMT\r\nContent-Type: application/json\r\nContent-Length: %d"
        self.error_body_template = '{"error_message": {"debuginfo": null, "faultcode": "PolicyEnforcer", "faultstring": "%s"}}'

    def test_request(self, a_request):
        """
        Test a request

        :param a_request: [str*] The request, as an array of strings
        :return: "" is pass the test, a string with explanation otherwise
        :rtype: str
        """
        if not self.identify_request(a_request):
            return ""

        self.apply_policy = True

        if not self.decide_fate(a_request):
            print("Request rejected.")
            return self.polish_error_message(self.error_body_template % self.gen_error_message())

        return ""

    def polish_error_message(self, body):
        """
        Generate the final error message, with both header and body.

        :param body: str The error body
        :return: The error Message
        :rtype: str
        """
        header = self.error_header_template % (asctime(gmtime()), len(body))
        return "%s\r\n\r\n%s" % (header, body)

    def identify_request(self, a_request):
        """
        Find out if the request is concerned by this policy.

        :param a_request: [str*] The request, as an array of strings
        :return: True if this policy manage it, False otherwise
        :rtype: bool
        """
        raise NotImplementedError

    def decide_fate(self, a_request):
        """
        Decide the fate of the request.

        :param a_request: [str*] The request, as an array of strings
        :return: True if it will be send to the API, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError

    def gen_error_message(self):
        """
        Generate an error message.

        Used in case of refused request.

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