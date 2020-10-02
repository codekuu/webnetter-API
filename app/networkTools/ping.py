#!/usr/bin/python3

###################
# Imports
import subprocess
###################


class ping:

    async def run(IPorHOSTNAME):

        hostname = IPorHOSTNAME
        param = '-c'
        command = ['ping', param, '1', hostname]
        response = subprocess.call(command) == 0

        if response is True or response is False:
            response_clean = response

        # RESPONSE
        pingData = {}
        pingData['host'] = hostname
        pingData['up'] = response_clean

        return pingData
