#!/usr/bin/env python

import socket
import re
import threading
import argparse

from time import sleep

from client_com import ClientCom
from api_com import APICom

from policy.alarm_quota import AlarmQuota
from policy.alarm_period import AlarmPeriod
from policy.sample_rate import SampleRate


class PolicyEnforcer():
    def __init__(self, listening_port, api_address, api_port, max_thread):
        """
        :param listening_port: int the port to access the policy enforcer
        :param api_address: str the address of the api
        :param api_port: int the port of the api
        :param max_thread: int The maximum of threads for the request processing.
        """
        self.ext_port = listening_port
        self.int_address = api_address
        self.int_port = api_port

        self.threads = []
        self.max_thread = max_thread

        self.policy_collection = [AlarmQuota(), AlarmPeriod(1200), SampleRate(5)]

        self.chaussette = self.create_chaussette()
        print("Init complete.")

    def create_chaussette(self):
        """
        Create the listening socket on self.ext_port.

        :return: Socket listening (up to 5 connections at the same time).
        :rtype: socket.socket
        """
        chaussette = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        chaussette.bind((socket.gethostname(), self.ext_port))

        chaussette.listen(self.max_thread)

        return chaussette

    def run(self):
        """
        Main loop to process requests.

        Wait for a request, then give the socket to the process_request method.
        Create a new thread for each request processed.

        If we got the maximum number of threads (self.max_thread), will wait until
        at least one of them is done.

        :return: Return nothing
        :rtype: None
        """
        print("Entering main loop.\nAwaiting for connections.")
        while True:
            self.trim_threads()
            if len(self.threads) >= self.max_thread:
                print("Max Threads (%d). Waiting for one to finish." % self.max_thread)
                sleep(1)
                continue

            (chaussette_client, address) = self.chaussette.accept()

            self.threads.append(threading.Thread(target=self.process_request, args=[chaussette_client]))
            self.threads[-1].start()

    def trim_threads(self):
        """
        Will remove the dead threads from the self.threads list.
        """
        for thread in self.threads:
            if not thread.is_alive():
                self.threads.remove(thread)

    def process_request(self, chaussette_client):
        """
        :param chaussette_client: socket.socket Socket from the client
        :return: None
        """
        client_com = ClientCom(chaussette_client, self.ext_port)
        api_com = APICom(self.int_address, self.int_port)

        request = client_com.receive_request()
        decision = self.test_request(request)

        response = api_com.get_response(request, decision, self.ext_port)
        self.analyze_response(response)

        client_com.send_response(response)

    def test_request(self, request):
        """
        Test the request for every policy in the collection (self.policy_collection)
        It will call their test_request methods.

        Stop at the first test that return a non empty string.

        :param request: str The request
        :return: "" if ok, String with explanation otherwise.
        :rtype: str
        """
        split_request = re.split('\r\n', request)

        for policy in self.policy_collection:
            result = policy.test_request(split_request)

            if result:
                return result

        return ""

    def analyze_response(self, response):
        """
        Will test the API response for each policy in the collection (self.policy_collection)
        It will call their analyze_response methods.

        Can be useful for quota system for instance: increment the utilization
        only if the response is not an error.

        :param response: str The response
        :rtype: None
        """
        for policy in self.policy_collection:
            policy.analyze_response(response)


# ##########################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-P", "--listening_port",
                        default=9001,
                        type=int,
                        dest="listening_port",
                        help="The port to listen.\nDefault is 9001.")
    parser.add_argument("-a", "--api_address",
                        default="qos107.research.att.com",
                        type=str,
                        dest="api_address",
                        help="The address of the API.")
    parser.add_argument("-p", "--api_port",
                        default="8777",
                        type=int,
                        dest="api_port",
                        help="The port of the API.\nDefault is 8777.")
    parser.add_argument("-t", "--max_thread",
                        default=5,
                        type=int,
                        dest="max_thread",
                        help="The maximum thread to process the requests.\nDefault is 5.")

    args = parser.parse_args()

    pe = PolicyEnforcer(listening_port=args.listening_port,
                        api_address=args.api_address,
                        api_port=args.api_port,
                        max_thread=args.max_thread)

    pe.run()