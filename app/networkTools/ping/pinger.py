#!/usr/bin/python3

###################
# Imports
import os
###################

class Pinger:

    def ping(IPorHOSTNAME):

        hostname = IPorHOSTNAME
        response = os.system("ping -c 1 " + hostname + " > /dev/null")

        if response == 0:
            responseMessage = True
        else:
            responseMessage = False

        # RESPONSE
        pingData = {}
        pingData['host'] = hostname
        pingData['up'] = responseMessage

        return pingData
