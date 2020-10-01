#!/usr/bin/python3
###################
# CONFIG FILE
###################

###################
# IMPORTS
import logging
###################


###################
# FLASK
backendHost = '0.0.0.0'  # Host Adress
indexFile = 'index.html'  # FLASK render_template
###################


###################
# GENERAL
# LOGGING
logger = logging.getLogger("webnetter")
hdlr = logging.FileHandler("webnetter.log")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Blacklist file
blackListFile = 'blacklistHosts.txt'

# Enable GUI
gui_enabled = True  # True / False

########################################################
# SCRIPT START OUTPUT
webnetterAPI_version = "2.0"
