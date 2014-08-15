#!/usr/bin/env python

import socket


class APICom():
    def __init__(self, api_address, api_port):
        """
        :param api_address: str The address of the API
        :param api_port: int The port of the API
        """
        self.address = api_address
        self.port = api_port
        self.chaussette = self.create_chaussette()

    def create_chaussette(self):
        """
        Create the socket to talk with the API.
        Use self.api_port and self.api_port

        :return: The socket
        :rtype: socket.socket
        """
        ch = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch.connect((self.address, self.port))

        return ch

    def send_request(self, request, listen_port):
        """
        Will send the request to the API.
        It will firstly adapt the request if needed, using the
        self.adapt_request function.

        :param request: str The request
        :param listen_port: int The listening port of the policy enforcer
        :return: The API response
        :rtype: str
        """

        request = self.adapt_request(request, listen_port)

        self.chaussette.send(request)

    def adapt_request(self, original_request, listen_port):
        """
        Adapt the request. Will replace the local address by the API address.

        :param original_request: str The original request.
        :param listen_port: int The PE listening port.
        :return: The new request
        :rtype: str
        """
        return original_request.replace("localhost:%d" % listen_port, "%s:%s" % (self.address, self.port))

    def receive_response(self):
        """
        Receive the response from the API, then return it.

        :return: The response
        :rtype: str
        """
        print("Waiting response on chaussure...")
        chunks = []

        while True:
            chunks.append(self.chaussette.recv(2048))

            if len(chunks[-1]) == 0:
                break

        self.chaussette.shutdown(socket.SHUT_RDWR)

        return ''.join(chunks)

    def get_response(self, request, decision, ext_port):
        """
        If the decision allow it, send the request to the API and return its response.
        Otherwise, return the decision, which is actually an error message.

        :param request: str
        :param decision: str The test decision. If different from "", request not processed, and is returned instead.
        :return: API response if decision is true, decision otherwise
        :rtype: str
        """
        if decision:
            return decision

        self.send_request(request, ext_port)

        return self.receive_response()