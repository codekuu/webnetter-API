#!/usr/bin/python3

# GENERAL IMPORTS
import os
import json
import base64
import settings

# NETMIKO
from netmiko import ConnectHandler


class execConfigure:

    # CONFIGURE START
    def execConf(data):

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
            raise Exception('No configuration file in the request.')

        configurationFile = data.files['file']

        if configurationFile.filename == '':
            raise Exception('No configuration file found.')

        if configurationFile and allowed_file(configurationFile.filename):
            for host in hosts:

                with open(blacklistHosts, 'r') as blacklist:
                    if host['host'] not in blacklist.read():

                        # CHECK THAT ALL KEYS ARE IN DATA
                        if all(key in host for key in ('username', 'password', 'device_type', 'port', 'host')):

                            # CREATE AND SAVE FILE LOCALY
                            savePath = os.getcwd() + '/networkTools/configure/CONFIGURATION_FOLDER/' + configurationFile.filename
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
                                net_connect = ConnectHandler(**connectData)
                                dataFromHardware = net_connect.send_config_from_file(config_file=savePath)
                                responseData['dataFromHost'] += '##### ' + host['host'] + ' #####\n\n' + dataFromHardware + '\n\n###########################\n\n'

                            except Exception as e:
                                info = str(e)
                                raise Exception(info)
                            net_connect.disconnect()

                        else:
                            raise Exception('Missing data in request.')

                    else:
                        responseData['dataFromHost'] += '##### ' + host['host'] + ' #####\n\n' + host['host'] + ' found in blacklist, wont do anything with this host.\n\n###########################\n\n'
        else:
            raise Exception('Allowed file type are txt.')

            # Close and remove file.
            configurationFile.close()
            os.remove(savePath)

        return responseData
