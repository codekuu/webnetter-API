#!/usr/bin/python3
###################
# CONFIG FILE
###################

###################
# IMPORTS
import os
import subprocess
###################


###################
# FLASK
backendHost = '0.0.0.0'  # Host Adress
indexFile = 'index.html'  # FLASK render_template
###################


###################
# GENERAL
file_directory_helper = os.path.dirname(__file__)
backendFilePath = file_directory_helper  # Filepath for the backend
logFile = file_directory_helper + '/server-calls.log'  # Logfile
blackListFile = 'blacklistHosts.txt'  # BlackList Host File

# Enable GUI
gui_enabled = True  # True / False

# Text FSM
useTextFSM = True  # Netmiko NTC template usage.
os.environ["NET_TEXTFSM"] = file_directory_helper + '/libs/ntc-templates/templates/'  # Create ENV for TextFSM
###################


###################
# TLS / SSL
ssl_enabled = False
fullchain = 'fullchain.pem'  # Use fullpath from app/
privkey = 'privkey.pem'  # Use fullpath from app/
###################


########################################################
# SCRIPT START OUTPUT
tmp = subprocess.call('clear', shell=True)
webnetterAPI_version = "2.0"

print(f"""
__          ________ ____  _   _ ______ _______ _______ ______ _____             _____ _____
\ \        / /  ____|  _ \| \ | |  ____|__   __|__   __|  ____|  __ \      /\   |  __ \_   _|
 \ \  /\  / /| |__  | |_) |  \| | |__     | |     | |  | |__  | |__) |    /  \  | |__) || |
  \ \/  \/ / |  __| |  _ <| . ` |  __|    | |     | |  |  __| |  _  /    / /\ \ |  ___/ | |
   \  /\  /  | |____| |_) | |\  | |____   | |     | |  | |____| | \ \   / ____ \| |    _| |_
    \/  \/   |______|____/|_| \_|______|  |_|     |_|  |______|_|  \_\ /_/    \_\_|   |_____|

Version: {webnetterAPI_version}
Author: Kevin Wiz Kuusela (Codekuu)
Github: https://github.com/codekuu/webnetter-api

GUI Enabled: {gui_enabled}
SSL Enabled: {ssl_enabled}
Hosting address: {backendHost}
Privkey: {backendFilePath}/{privkey}
Fullchain.pem: {backendFilePath}/{fullchain}


""")
########################################################
