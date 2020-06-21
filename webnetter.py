#!/usr/bin/python3

import os
import datetime
import config

######################################
# BACKEND FILES
from backend.networkTools.ping.pinger import Pinger as pingHost
from backend.networkTools.runcommand.execCustomCommand import execCustomCommand as commandAPI
from backend.networkTools.configure.execConfigure import execConfigure as confAPI
from backend.networkTools.scp.scpFile import sendFile as scpAPI


###################
#  FLASK
from flask import Flask, jsonify, request, render_template
######################################


app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")

###################
# BACKEND
os.chdir(config.backendFilePath)  # Backend Filepath from config.py
blacklistHosts = os.path.join(config.blackListFile)  # Blacklist from config.py


###################
# LOGGER
def dataLogger(IPaddress, requestData, call):
    logFile = open(config.logFile, "a")  # In config.py
    dateNtime = datetime.datetime.now()
    logFile.write(str(dateNtime) + " - " + IPaddress + " - " + requestData + ' - ' + call + "\n")


####################
# START / ROUTE
if config.gui_enabled:  # Enables frontend gui
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template(config.indexFile)  # In config.py
else:
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        dataLogger(request.remote_addr, str(request), 'Path: /')
        return jsonify({"status": "success", "name": "Webnetter API", "version": "1.0", "message": "Documentation can be found at www.webnetter.net", "online": "true"})


###################
# PING
@app.route("/webnetter/ping/<string:hostname>", methods=['GET'])
def getICMP(hostname):
    with open(blacklistHosts, 'r') as blacklist:
        if hostname in blacklist.read():
            return jsonify({"status": "error", "message": "Host exist in blacklist."})

        if request.remote_addr not in blacklist.read():
            if request.method == 'GET':
                try:
                    call = pingHost.ping(hostname)
                    dataLogger(request.remote_addr, str(request), str(call))
                    return jsonify({"status": "success", "data": call})

                except Exception as e:
                    print(e)
                    dataLogger(request.remote_addr, str(request), 'Failed due to: ' + str(e))
                    return jsonify({"status": "fail", "message": "Operation failed, try again or contact admin."})
            else:
                return jsonify({"status": "error", "message": "No endpoint matching request."})
        else:
            return jsonify({"status": "error", "message": "Host exist in blacklist."})


###################
# RUN COMMAND
@app.route("/webnetter/runcommands", methods=['POST'])
def connect():
    with open(blacklistHosts, 'r') as blacklist:
        if request.remote_addr not in blacklist.read():

            if request.method == 'POST':
                try:
                    call = commandAPI.ecc(request)
                    dataLogger(request.remote_addr, str(request), str(call))
                    return jsonify({"status": "success", "data": call})

                except Exception as e:
                    print(e)
                    dataLogger(request.remote_addr, str(request), 'Failed due to: ' + str(e))
                    return jsonify({"status": "fail", "message": "Operation failed, try again or contact admin."})
            else:
                return jsonify({"status": "error", "message": "No endpoint matching request."})
        else:
            return jsonify({"status": "error", "message": "Host exist in blacklist."})


###################
# CONFIGURE
@app.route("/webnetter/configure", methods=['POST'])
def configure():
    with open(blacklistHosts, 'r') as blacklist:
        if request.remote_addr not in blacklist.read():

            if request.method == 'POST':
                try:
                    call = confAPI.execConf(request)
                    dataLogger(request.remote_addr, str(request), str(call))
                    return jsonify({"status": "success", "data": call})

                except Exception as e:
                    print(e)
                    dataLogger(request.remote_addr, str(request), 'Failed due to: ' + str(e))
                    return jsonify({"status": "fail", "message": "Operation failed, try again or contact admin."})
            else:
                return jsonify({"status": "error", "message": "No endpoint matching request."})
        else:
            return jsonify({"status": "error", "message": "Host exist in blacklist."})


###################
# scp
@app.route("/webnetter/scp", methods=['POST'])
def scp():
    with open(blacklistHosts, 'r') as blacklist:
        if request.remote_addr not in blacklist.read():

            if request.method == 'POST':
                try:
                    call = scpAPI.execSCP(request)
                    dataLogger(request.remote_addr, str(request), str(call))
                    return jsonify({"status": "success", "data": call})

                except Exception as e:
                    print(e)
                    dataLogger(request.remote_addr, str(request), 'Failed due to: ' + str(e))
                    return jsonify({"status": "fail", "message": "Operation failed, try again or contact admin."})
            else:
                return jsonify({"status": "error", "message": "No endpoint matching request."})
        else:
            return jsonify({"status": "error", "message": "Host exist in blacklist."})


if __name__ == "__main__":
    if config.ssl_enabled:  # Change this in Settings.py
        app.run(host=config.backendHost, ssl_context=(config.fullchain, config.privkey))
    else:
        app.run(host=config.backendHost)
