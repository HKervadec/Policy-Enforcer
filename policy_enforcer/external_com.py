#!/usr/bin/env python

import socket
import re


class ExternalManager():
    def __init__(self, chaussette_client, ext_port=9001):
        """
        :param ext_port: int The port to listen
        """
        self.ext_port = ext_port
        self.chaussette_client = chaussette_client

    def receive_request(self):
        """
        Receive the request on the self.chaussette_client socket

        :return: The request
        :rtype: str
        """
        print("Receiving the request...")
        str_request = ""

        while True:
            str_request += self.chaussette_client.recv(2048)

            try:
                if self.analyze_request(str_request):
                    break
            except AttributeError:
                pass

        return str_request

    @staticmethod
    def analyze_request(request):
        """
        Test if the received request if complete.

        :param request: The request to test
        :return: True if complete, False otherwise
        :rtype: bool
        """
        if not '\r\n\r\n' in request:
            return False

        splitted = re.split(r'\r\n', request)

        for item in splitted:
            grouped = re.match(r"Content-Length: (\d+)", item)
            if grouped:
                size = int(grouped.group(1))
                real_size = len(splitted[-1])

                return real_size == size

        return True

    def send_response(self, response):
        """
        Send the response to the client (self.chaussette_client).

        :param response: str The response
        :rtype: None
        """
        self.chaussette_client.send(response)
        self.chaussette_client.shutdown(socket.SHUT_RDWR) # Always shut down your chaussette