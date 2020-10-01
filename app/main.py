#!/usr/bin/python3

import os
import config
import json

######################################
# BACKEND FILES
from networkTools.ping import ping
from networkTools.runcommand import runcommand
from networkTools.configure import configure
from networkTools.scp import scp

###################
#  FastAPI & Starlette
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, JSONResponse
#
from basemodels import model_response_ping, model_response_general, model_request_runcommands
# Async
import asyncio
###################

if config.swagger_enabled:
    app = FastAPI(
        title="Webnetter API",
        description="Plug and Play Network Management API built on Docker, fastAPI & Netmiko with optional GUI.",
        version=config.webnetterAPI_version,
        redoc_url=None
        )
else:
    app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="dist/static"), name="static")


###################
# BACKEND
blacklistHosts = os.path.join(config.blackListFile)  # Blacklist from config.py


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
        config.logger.info(f"{request.client.host} {request.url.path} Path: /")
        return {"status": "success", "name": "Webnetter API", "version": config.webnetterAPI_version, "message": "Documentation can be found at https://github.com/codekuu/webnetter-api", "online": True}


"""
###################################
###########     PING    ###########
###################################
"""


@app.get("/webnetter/ping/{hostname}", response_model=model_response_ping)
def getICMP(request: Request, hostname: str):
    try:
        call = asyncio.run(ping.run(hostname))
        config.logger.info(f"{request.client.host} {request.url.path} {call}")
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": call}
        )

    except Exception as e:
        config.logger.warning(f"{request.client.host} {request.url.path} {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "fail", "message": "Operation failed, check logging for more information."},
        )


"""
###################################
########### RUN COMMAND ###########
###################################
"""


@app.post("/webnetter/runcommands", response_model=model_response_general)
def run_commands_on_hosts(request: Request, hosts: model_request_runcommands):
    try:
        hosts_dict = hosts.dict()
        call = asyncio.run(runcommand.run(request, hosts_dict['hosts']))
        config.logger.info(f"{request.client.host} {request.url.path} {call}")

        # Put output from all hosts in one string
        output_from_all = ""
        for data in call:
            fixed_data = data['output'].replace("\n", f"\n[{data['host']} {data['software']}] ")
            output_from_all += f"[{data['host']} {data['software']}] {fixed_data}\n"

        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": call, "outputFromAll": f'{output_from_all}\n'}
        )

    except Exception as e:
        config.logger.warning(f"{request.client.host} {request.url.path} {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "fail", "message": "Operation failed, check logging for more information."},
        )


"""
###################################
###########  CONFIGURE  ###########
###################################
"""


@app.post("/webnetter/configure", response_model=model_response_general)
def configure_hosts(request: Request, hosts: str = Form(...), file: UploadFile = File(...)):
    try:
        json_hosts = json.loads(hosts)
        call = asyncio.run(configure.run(request, json_hosts, file))
        config.logger.info(f"{request.client.host} {request.url.path} {call}")

        # Put output from all hosts in one string
        output_from_all = ""
        for data in call:
            fixed_data = data['output'].replace("\n", f"\n[{data['host']} {data['software']}] ")
            output_from_all += f"[{data['host']} {data['software']}] {fixed_data}\n"

        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": call, "outputFromAll": f'{output_from_all}\n'}
        )

    except Exception as e:
        config.logger.warning(f"{request.client.host} {request.url.path} {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "fail", "message": "Operation failed, check logging for more information."},
        )


"""
###################################
###########     SCP     ###########
###################################
"""


@app.post("/webnetter/scp", response_model=model_response_general)
def scp_file_to_hosts(request: Request, hosts: str = Form(...), file: UploadFile = File(...)):
    try:
        json_hosts = json.loads(hosts)
        call = asyncio.run(scp.run(request, json_hosts, file))
        config.logger.info(f"{request.client.host} {request.url.path} {call}")

        # Put output from all hosts in one string
        output_from_all = ""
        for data in call:
            fixed_data = data['output'].replace("\n", f"\n[{data['host']} {data['software']}] ")
            output_from_all += f"[{data['host']} {data['software']}] {fixed_data}\n"

        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": call, "outputFromAll": f'{output_from_all}\n'}
        )

    except Exception as e:
        config.logger.warning(f"{request.client.host} {request.url.path} {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "fail", "message": "Operation failed, check logging for more information."},
        )
