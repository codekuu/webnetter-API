#!/usr/bin/python3
###################
# CONFIG FILE
###################

###################
# IMPORTS
import logging
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
swagger_enabled = True  # True / False

########################################################
# SCRIPT START OUTPUT
webnetterAPI_version = "2.1"
