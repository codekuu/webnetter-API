#!/usr/bin/python3

# GENERAL IMPORTS
import base64
import settings

# NETMIKO
from netmiko import ConnectHandler

class execCustomCommand:

    # Run CLI-Command
    def ecc(data):
        if all(key in data.json for key in ("host", "username", "password", "device_type", "port", "command")):
            host = data.json['host']
            username = data.json['username']
            password = data.json['password']
            passwordClean = base64.b64decode(password).decode('ascii')
            device_type = data.json['device_type']
            port = data.json['port'] or 22
            commandToExec = data.json['command']

            responseData = {}

            connectData = {
                'device_type': device_type,
                'host': host,
                'username': username,
                'password': passwordClean,
                'port': port,  # Defaults to 22
                'global_delay_factor': 0.2
            }

            try:
                net_connect = ConnectHandler(**connectData)
                response = net_connect.send_command(commandToExec, use_textfsm=settings.useTextFSM)
                responseData['dataFromHost'] = response
                net_connect.disconnect()

                return responseData

            except Exception as e:
                info = str(e)
                raise Exception(info)

        else:
            raise Exception("Missing data in POST call.")
