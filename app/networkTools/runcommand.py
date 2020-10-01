#!/usr/bin/python3

# GENERAL IMPORTS
import os
import base64
import config

# NETMIKO
from netmiko import ConnectHandler


class runcommand:

    async def run(request, hosts):

        ###################
        # BACKEND
        blacklistHosts = os.path.join(config.blackListFile)  # Blacklist from config.py
        ############################

        # Setting standard Request Message
        responseData = []

        for host in hosts:

            # CHECK IF PASSWORD IS BASE64
            try:
                base64.b64encode(base64.b64decode(host['password'])) == host['password']
            except Exception:
                responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Password has to be encoded with base64 before process.'})
                continue

            with open(blacklistHosts, 'r') as blacklist:

                try:
                    if host['host'] not in blacklist.read():

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
                            response = net_connect.send_command(host['command'])
                            net_connect.disconnect()
                            responseData.append({'success': True, 'host': host['host'], 'software': host['device_type'], 'output': response})

                        except Exception as error_message:
                            info = str(error_message)
                            config.logger.warning(f"{host['host']} {info}")
                            responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': info})

                    else:
                        responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Host blacklisted.'})

                except Exception as error_message:
                    info = str(error_message)
                    config.logger.warning(f"{host['host']} {info}")
                    responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': info})

        return responseData
