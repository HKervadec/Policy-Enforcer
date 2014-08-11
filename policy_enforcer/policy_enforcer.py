#!/usr/bin/env python

from external_com import ExternalManager
from internal_com import InternalManager

from policy.quota_alarm import QuotaAlarm
from policy.sample_rate import SampleRate

import socket
import re


class PolicyEnforcer():
    def __init__(self, ext_port=9001,
                 int_address='qos107.research.att.com',
                 int_port=8777):
        """
        :param ext_port: int the port to access the policy enforcer
        :param int_address: str the address of the api
        :param int_port: int the port of the api
        """
        self.ext_port = ext_port
        self.int_address = int_address
        self.int_port = int_port

        self.policy_collection = [QuotaAlarm(), SampleRate(1)]

        self.chaussette = self.create_chaussette()

    def create_chaussette(self):
        """
        Create the listening socket on self.ext_port.

        :return: Socket listening (up to 5 connections at the same time).
        :rtype: socket.socket
        """
        chaussette = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        chaussette.bind((socket.gethostname(), self.ext_port))

        chaussette.listen(5)

        return chaussette

    def run(self):
        """
        Main loop to process requests.

        Wait for a request, then give the socket to the process_request method.

        :return: Return nothing
        :rtype: None
        """
        while True:
            (chaussette_client, address) = self.chaussette.accept()

            self.process_request(chaussette_client)

    def process_request(self, chaussette_client):
        """
        :param chaussette_client: socket.socket Socket from the client
        :return: None
        """
        ext_manager = ExternalManager(chaussette_client, self.ext_port)
        int_manager = InternalManager(self.int_address, self.int_port)

        request = ext_manager.receive_request()
        decision = self.test_request(request)

        response = int_manager.get_response(request, decision, self.ext_port)
        self.test_response(response)

        print("Sending response...")
        ext_manager.send_response(response)

    def test_request(self, request):
        """
        Test the request for every policy in the collection (self.policy_collection)
        It will call their test_request methods.

        Will do every test, even if one already said no.

        :param request: str The request
        :return: True if pass all the test, False otherwise
        :rtype: bool
        """
        split_request = re.split('\r\n', request)

        result = True

        for policy in self.policy_collection:
            if not policy.test_request(split_request):
                result = False

        return result

    def test_response(self, response):
        """
        Will test the API response for each policy in the collection (self.policy_collection)
        It will call their test_response methods.

        Can be useful for quota system for instance: increment the utilization
        only if the response is not an error.

        :param response: str The response
        :rtype: None
        """

        for policy in self.policy_collection:
            policy.test_response(response)


# ##########################
if __name__ == "__main__":
    pe = PolicyEnforcer()

    pe.run()