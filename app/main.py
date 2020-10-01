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
    try:
        call = pingHost.ping(hostname)
        dataLogger(request.client.host, request.body(), str(call))
        return {"status": "success", "data": call}

    except Exception as e:
        dataLogger(request.client.host, request.body(), 'Failed due to: ' + str(e))
        return {"status": "fail", "message": "Operation failed, try again or contact admin."}


###################
# RUN COMMAND
@app.post("/webnetter/runcommands")
def run_commands_on_hosts(request: Request, hosts: Runcommands_model):
    try:
        hosts_dict = hosts.dict()
        call = asyncio.run(commandAPI.ecc(request, hosts_dict['hosts']))
        dataLogger(request.client.host, request.body(), str(call))
        return {"status": "success", "data": call}

    except Exception as e:
        dataLogger(request.client.host, request.body(), 'Failed due to: ' + str(e))
        return {"status": "fail", "message": "Operation failed, try again or contact admin."}


###################
# CONFIGURE
@app.post("/webnetter/configure")
def configure_hosts(request: Request, hosts: str = Form(...), file: UploadFile = File(...)):
    try:
        json_hosts = json.loads(hosts)
        call = asyncio.run(confAPI.execConf(request, json_hosts, file))
        dataLogger(request.client.host, request.body(), str(call))
        return {"status": "success", "data": call}

    except Exception as e:
        dataLogger(request.client.host, request.body(), 'Failed due to: ' + str(e))
        return {"status": "fail", "message": "Operation failed, try again or contact admin."}


###################
# SCP
@app.post("/webnetter/scp")
def scp_file_to_hosts(request: Request, hosts: str = Form(...), file: UploadFile = File(...)):
    try:
        json_hosts = json.loads(hosts)
        call = asyncio.run(scpAPI.execSCP(request, json_hosts, file))
        dataLogger(request.client.host, request.body(), str(call))
        return {"status": "success", "data": call}

    except Exception as e:
        dataLogger(request.client.host, request.body(), 'Failed due to: ' + str(e))
        return {"status": "fail", "message": "Operation failed, try again or contact admin."}
