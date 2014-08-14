#!/usr/bin/env python

import socket


class InternalManager():
    def __init__(self, int_address, int_port):
        """
        :param int_address: str The address of the API
        :param int_port: int The port of the API
        """
        self.address = int_address
        self.port = int_port
        self.chaussette = self.create_chaussette()

    def send_request(self, request, ext_port):
        """
        Will send the request to the API.
        It will firstly adapt the request if needed, using the
        self.adapt_request function.

        :param request: str The request
        :param ext_port: int The original port of the quota manager
        :return: The API response
        :rtype: str
        """

        request = self.adapt_request(request, ext_port)

        print(repr(request))
        self.chaussette.send(request)

    def adapt_request(self, original_request, ext_port=9001):
        """
        Adapt the request. Will replace the local address by the API address.

        :param original_request: str The original request.
        :param ext_port: int The original external port.
        :return: The new request
        :rtype: str
        """
        new_request = original_request.replace("localhost:%d" % ext_port, "%s:%s" % (self.address, self.port))

        return new_request

    def create_chaussette(self):
        """
        Create the socket to talk with the API.
        Use self.int_port and self.int_port

        :return: The socket
        :rtype: socket.socket
        """
        ch = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ch.connect((self.address, self.port))

        return ch

    def receive_response(self):
        """
        Receive the response from the API, then return it.

        :return: The response
        :rtype: str
        """
        print("Waiting response on chaussette...")
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
        Otherwise, return a predefined string.

        :param request: str
        :param decision: str The test decision. If different from "", request not processed, and return it instead.
        :return: API response if decision is true, decision otherwise
        :rtype: str
        """
        if decision:
            return decision

        self.send_request(request, ext_port)

        return self.receive_response()