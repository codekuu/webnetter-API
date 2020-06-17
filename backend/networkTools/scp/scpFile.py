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
        responseData = {}
        responseData['dataFromHost'] = ''
        # Allowed file extensions
        ALLOWED_EXTENSIONS = set(['txt', 'conf', 'cfg'])

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # EXATRACTING DATA FROM REQUEST
        hostsDict = data.form.to_dict()
        hosts = json.loads(hostsDict['hostData'])
        # CHECK IF FILE EXIST IN REQUEST
        if 'file' not in data.files:
            raise Exception('No file in request.')

        configurationFile = data.files['file']

        if configurationFile.filename == '':
            raise Exception('No file found.')

        if configurationFile and allowed_file(configurationFile.filename):
            for host in hosts:

                with open(blacklistHosts, 'r') as blacklist:
                    if host['host'] not in blacklist.read():
                        # CHECK THAT ALL KEYS ARE IN DATA
                        if all(key in host for key in ('username', 'password', 'device_type', 'port', 'host', 'location')):

                            # CREATE AND SAVE FILE LOCALY
                            savePath = os.getcwd() + '/networkTools/scp/CONFIGURATION_FOLDER/' + configurationFile.filename
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
                                responseData['dataFromHost'] += '##### ' + host['host'] + ' #####\n\n'
                                if dataFromHost['file_verified']:
                                    if dataFromHost['file_exists']:
                                        if not dataFromHost['file_transferred']:
                                            responseData['dataFromHost'] += 'Could not transfer file, it already exist in ' + host['location'] + '.'
                                    else:
                                        responseData['dataFromHost'] += configurationFile.filename + ' was transferred and verified.'
                                else:
                                    responseData['dataFromHost'] += 'We could not verify file transfer, check manually.'

                                responseData['dataFromHost'] += '\n\n###########################\n\n'

                            except Exception as e:
                                info = str(e)
                                raise Exception(info)

                            net_connect.disconnect()
                        else:
                            raise Exception('Missing data in request.')
                    else:
                        responseData['dataFromHost'] += '##### ' + host['host'] + ' #####\n\n' + host['host'] + ' found in blacklist, wont do anything with this host.\n\n###########################\n\n'

        else:
            raise Exception('Allowed file types are ' + ALLOWED_EXTENSIONS)

        # Close and remove file.
        configurationFile.close()
        os.remove(savePath)

        return responseData
