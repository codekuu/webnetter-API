#!/usr/bin/python3

###################
# Imports
import os
###################


class ping:

    async def run(IPorHOSTNAME):

        hostname = IPorHOSTNAME
        response = os.system(f"ping -c 1 {hostname} > /dev/null")

        if response == 0:
            responseMessage = True
        else:
            responseMessage = False

        # RESPONSE
        pingData = {}
        pingData['host'] = hostname
        pingData['up'] = responseMessage

        return pingData
