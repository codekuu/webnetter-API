#!/usr/bin/python3

# GENERAL IMPORTS
import os
import json
import base64
import settings

# NETMIKO
from netmiko import ConnectHandler


class execCustomCommand:

    # SEND COMMAND START
    def ecc(data):

        ###################
        # BACKEND
        os.chdir(settings.backendFilePath)  # Backend Filepath from settings.py
        blacklistHosts = os.path.join(settings.blackListFile)  # Blacklist from settings.py
        ############################

        # Setting standard Request Message
        responseData = []

        # EXATRACTING DATA FROM REQUEST
        # hostsDict = data.json.to_dict()
        hosts = json.loads(data.json['hosts'])
        for host in hosts:
            with open(blacklistHosts, 'r') as blacklist:
                try:
                    if host['host'] not in blacklist.read():

                        # CHECK THAT ALL KEYS ARE IN DATA
                        if all(key in host for key in ('host', 'port', 'device_type', 'username', 'password', 'command')):

                            # CONNECTION DATA
                            connectData = {
                                'device_type': host['device_type'],
                                'host': host['host'],
                                'username': host['username'],
                                'password': base64.b64decode(host['password']).decode('ascii'),
                                'port': host['port']
                            }
                            try:
                                # OPERATION
                                net_connect = ConnectHandler(**connectData)
                                response = net_connect.send_command(host['command'], use_textfsm=settings.useTextFSM)
                                responseData.append({'success': True, 'host': host['host'], 'software': host['device_type'], 'output': response})

                            except Exception as error_message:
                                info = str(error_message)
                                print(host['host'] + " - " + info)
                            net_connect.disconnect()

                        else:
                            responseData.append({'success': False, 'host': host['host'], 'output': 'Missing data in request.'})

                    else:
                        responseData.append({'success': False, 'host': host['host'], 'output': 'Host blacklisted.'})
                except Exception as error_message:
                    info = str(error_message)
                    print(host['host'] + " - " + info)
                    raise Exception({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Something went wrong with processing this host, check Webnetter console.'})

        return responseData
