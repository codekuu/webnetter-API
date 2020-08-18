#!/usr/bin/python3

# GENERAL IMPORTS
import os
import base64
import config

# NETMIKO
from netmiko import ConnectHandler, file_transfer


class sendFile:

    # CONFIGURE START
    async def execSCP(request, hosts, file):

        ###################
        # BACKEND
        blacklistHosts = os.path.join(config.blackListFile)  # Blacklist from config.py
        ############################

        # Setting standard Request Message
        responseData = []

        # READ THE DATA FROM FILE
        configurationFileContentBytes = await file.read()
        confugrationFileContent = configurationFileContentBytes.decode('utf-8')

        if confugrationFileContent == '':
            raise Exception('No configuration file found.')

        for host in hosts:

            with open(blacklistHosts, 'r') as blacklist:
                try:
                    if host['host'] not in blacklist.read():
                        # CHECK THAT ALL KEYS ARE IN DATA
                        if all(key in host for key in ('username', 'password', 'device_type', 'port', 'host', 'location')):

                            savePath = os.path.dirname(__file__) + file.filename
                            with open(savePath, "w") as temp_file:
                                temp_file.write(confugrationFileContent)

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
                                dataFromHost = file_transfer(net_connect, source_file=savePath, dest_file=file.filename, file_system=host['location'], direction='put', overwrite_file=False)
                                net_connect.disconnect()

                                if dataFromHost['file_verified']:
                                    if dataFromHost['file_exists']:
                                        if dataFromHost['file_transferred']:
                                            responseData.append({'success': True, 'host': host['host'], 'software': host['device_type'], 'output': file.filename + ' was transferred and verified.'})
                                        else:
                                            responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Could not transfer file, it already exist in ' + host['location'] + '.'})
                                    else:
                                        responseData.append({'success': True, 'host': host['host'], 'software': host['device_type'], 'output': file.filename + ' was transferred and verified.'})
                                else:
                                    responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'We could not verify file transfer, check manually.'})

                            except Exception as error_message:
                                info = str(error_message)
                                print(host['host'] + " - " + info)
                                responseData.append({'success': False, 'host': host['host'], 'output': info})

                            # Close and remove file.
                            os.remove(savePath)

                        else:
                            responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Missing data in request.'})
                    else:
                        responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Host blacklisted.'})

                except Exception as error_message:
                    info = str(error_message)
                    print(host['host'] + " - " + info)
                    responseData.append({'success': False, 'host': host['host'], 'output': info})

        return responseData
