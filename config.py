#!/usr/bin/python3
###################
# SETTINGS FILE
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
fullchain = '../cert/fullchain.pem'  # Place the files in backend/cert/
privkey = '../cert/privkey.pem'  # Place the files in backend/cert/
###################


########################################################
# SCRIPT START OUTPUT
tmp = subprocess.call('clear', shell=True)

print("""
__          ________ ____  _   _ ______ _______ _______ ______ _____             _____ _____
\ \        / /  ____|  _ \| \ | |  ____|__   __|__   __|  ____|  __ \      /\   |  __ \_   _|
 \ \  /\  / /| |__  | |_) |  \| | |__     | |     | |  | |__  | |__) |    /  \  | |__) || |
  \ \/  \/ / |  __| |  _ <| . ` |  __|    | |     | |  |  __| |  _  /    / /\ \ |  ___/ | |
   \  /\  /  | |____| |_) | |\  | |____   | |     | |  | |____| | \ \   / ____ \| |    _| |_
    \/  \/   |______|____/|_| \_|______|  |_|     |_|  |______|_|  \_\ /_/    \_\_|   |_____|

Version: 1.0
Author: Kevin Wiz Kuusela (Codekuu)
Github: https://github.com/codekuu/webnetter-api
""")
print("GUI Enabled: " + str(gui_enabled))
print("Hosting address: " + backendHost)
print("")
print("SSL Enabled: " + str(ssl_enabled))
print("Fullchain.pem: " + backendFilePath + "/" + fullchain)
print("Privkey: " + backendFilePath + "/" + privkey)
print("")
print("")
########################################################
