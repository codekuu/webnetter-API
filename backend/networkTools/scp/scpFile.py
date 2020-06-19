#!/usr/bin/python3

# GENERAL IMPORTS
import os
import json
import base64
import settings

# NETMIKO
from netmiko import ConnectHandler, file_transfer


class sendFile:

    # CONFIGURE START
    def execSCP(data):

        ###################
        # BACKEND
        os.chdir(settings.backendFilePath)  # Backend Filepath from settings.py
        blacklistHosts = os.path.join(settings.blackListFile)  # Blacklist from settings.py
        ############################

        # Setting standard Request Message
        responseData = []

        # Allowed file extensions
        ALLOWED_EXTENSIONS = set(['txt', 'conf', 'cfg'])

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # EXATRACTING DATA FROM REQUEST
        hostsDict = data.form.to_dict()
        hosts = json.loads(hostsDict['hosts'])

        # CHECK IF FILE EXIST IN REQUEST
        if 'file' not in data.files:
            raise Exception('No file in request.')

        configurationFile = data.files['file']

        if configurationFile.filename == '':
            raise Exception('No file found.')

        if configurationFile and allowed_file(configurationFile.filename):
            for host in hosts:

                with open(blacklistHosts, 'r') as blacklist:
                    try:
                        if host['host'] not in blacklist.read():
                            # CHECK THAT ALL KEYS ARE IN DATA
                            if all(key in host for key in ('username', 'password', 'device_type', 'port', 'host', 'location')):

                                # CREATE AND SAVE FILE LOCALY
                                savePath = os.path.dirname(__file__) + configurationFile.filename
                                configurationFile.save(savePath, buffer_size=16384)

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
                                    direction = 'put'
                                    net_connect = ConnectHandler(**connectData)
                                    dataFromHost = file_transfer(net_connect, source_file=savePath, dest_file=configurationFile.filename, file_system=host['location'], direction=direction, overwrite_file=False)
                                    if dataFromHost['file_verified']:
                                        if dataFromHost['file_exists']:
                                            if dataFromHost['file_transferred']:
                                                responseData.append({'success': True, 'host': host['host'], 'software': host['device_type'], 'output': configurationFile.filename + ' was transferred and verified.'})
                                            else:
                                                responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Could not transfer file, it already exist in ' + host['location'] + '.'})
                                        else:
                                            responseData.append({'success': True, 'host': host['host'], 'software': host['device_type'], 'output': configurationFile.filename + ' was transferred and verified.'})
                                    else:
                                        responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'We could not verify file transfer, check manually.'})

                                except Exception as error_message:
                                    info = str(error_message)
                                    print(host['host'] + " - " + info)
                                net_connect.disconnect()

                                net_connect.disconnect()
                            else:
                                responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Missing data in request.'})
                        else:
                            responseData.append({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Host blacklisted.'})
                    except Exception as error_message:
                        info = str(error_message)
                        print(host['host'] + " - " + info)
                        raise Exception({'success': False, 'host': host['host'], 'software': host['device_type'], 'output': 'Something went wrong with processing this host, check Webnetter console.'})
        else:
            raise Exception('Allowed file types are ' + ALLOWED_EXTENSIONS)

        # Close and remove file.
        configurationFile.close()
        os.remove(savePath)

        return responseData
