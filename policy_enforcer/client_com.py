#!/usr/bin/env python

import socket
import re


class ClientCom():
    def __init__(self, chaussette_client):
        """
        :chaussette_client: socket.socket The socket connected to the client.
        """
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

        print(repr(str_request))
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

        parts = re.split(r'\r\n', request)

        for item in parts:
            grouped = re.match(r"Content-Length: (\d+)", item)
            if grouped:
                size = int(grouped.group(1))
                real_size = len(parts[-1])

                return real_size == size

        return True

    def send_response(self, response):
        """
        Send the response to the client (self.chaussette_client).

        :param response: str The response
        :rtype: None
        """
        print("Sending response...")

        self.chaussette_client.send(response)
        self.chaussette_client.shutdown(socket.SHUT_RDWR) # Always shut down your chaussette

        print(repr(response))
