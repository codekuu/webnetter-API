#!/usr/bin/python3

import os
import datetime
import config
import json

######################################
# BACKEND FILES
from networkTools.ping.pinger import Pinger as pingHost
from networkTools.runcommand.execCustomCommand import execCustomCommand as commandAPI
from networkTools.configure.execConfigure import execConfigure as confAPI
from networkTools.scp.scpFile import sendFile as scpAPI

###################
#  FastAPI & Pydantic
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles  # Frontend
from starlette.responses import FileResponse  # Frontend
#
from basemodels import Runcommands_model
# Async
import asyncio
###################

app = FastAPI()
app.mount("/static", StaticFiles(directory="dist/static"), name="static")


###################
# BACKEND
blacklistHosts = os.path.join(config.blackListFile)  # Blacklist from config.py


###################
# LOGGER
def dataLogger(IPaddress, requestData, call):
    logFile = open(config.logFile, "a")  # In config.py
    dateNtime = datetime.datetime.now()
    logFile.write(str(dateNtime) + " - " + IPaddress + " - " + str(requestData) + ' - ' + call + "\n")


####################
# START / ROUTE
if config.gui_enabled:  # Enables frontend gui
    @app.get("/")
    @app.get("/{path}")
    async def send_frontend():
        return FileResponse('./dist/index.html')
else:
    @app.get("/")
    async def send_frontend_api(request: Request):
        dataLogger(request.client.host, request.body(), 'Path: /')
        return {"status": "success", "name": "Webnetter API", "version": config.webnetterAPI_version, "message": "Documentation can be found at https://github.com/codekuu/webnetter-api", "online": "true"}


###################
# PING
@app.get("/webnetter/ping/{hostname}")
def getICMP(request: Request, hostname: str):
    with open(blacklistHosts, 'r') as blacklist:
        if hostname in blacklist.read():
            return {"status": "error", "message": "Host exist in blacklist."}

        if request.client.host not in blacklist.read():
            try:
                call = pingHost.ping(hostname)
                dataLogger(request.client.host, request.body(), str(call))
                return {"status": "success", "data": call}

            except Exception as e:
                dataLogger(request.client.host, request.body(), 'Failed due to: ' + str(e))
                return {"status": "fail", "message": "Operation failed, try again or contact admin."}
        else:
            return {"status": "error", "message": "Host exist in blacklist."}


###################
# RUN COMMAND
@app.post("/webnetter/runcommands")
def run_commands_on_hosts(request: Request, hosts: Runcommands_model):
    hosts_dict = hosts.dict()
    with open(blacklistHosts, 'r') as blacklist:
        if request.client.host not in blacklist.read():
            call = asyncio.run(commandAPI.ecc(request, hosts_dict['hosts']))
            dataLogger(request.client.host, request.body(), str(call))
            return {"status": "success", "data": call}

        else:
            return {"status": "error", "message": "Host exist in blacklist."}


###################
# CONFIGURE
@app.post("/webnetter/configure")
def configure_hosts(request: Request, hosts: str = Form(...), file: UploadFile = File(...)):
    with open(blacklistHosts, 'r') as blacklist:
        if request.client.host not in blacklist.read():
            try:
                json_hosts = json.loads(hosts)
                call = asyncio.run(confAPI.execConf(request, json_hosts, file))
                dataLogger(request.client.host, request.body(), str(call))
                return {"status": "success", "data": call}

            except Exception as e:
                dataLogger(request.client.host, request.body(), 'Failed due to: ' + str(e))
                return {"status": "fail", "message": "Operation failed, try again or contact admin."}
        else:
            return {"status": "error", "message": "Host exist in blacklist."}


###################
# SCP
@app.post("/webnetter/scp")
def scp_file_to_hosts(request: Request, hosts: str = Form(...), file: UploadFile = File(...)):
    with open(blacklistHosts, 'r') as blacklist:
        if request.client.host not in blacklist.read():
            try:
                json_hosts = json.loads(hosts)
                call = asyncio.run(scpAPI.execSCP(request, json_hosts, file))
                dataLogger(request.client.host, request.body(), str(call))
                return {"status": "success", "data": call}

            except Exception as e:
                dataLogger(request.client.host, request.body(), 'Failed due to: ' + str(e))
                return {"status": "fail", "message": "Operation failed, try again or contact admin."}
        else:
            return {"status": "error", "message": "Host exist in blacklist."}


if __name__ == "__main__":
    if config.ssl_enabled:  # Change this in Settings.py
        app.run(host=config.backendHost, ssl_context=(config.fullchain, config.privkey))
    else:
        app.run(host=config.backendHost)
