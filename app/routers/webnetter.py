import json
from fastapi import APIRouter, Request, File, UploadFile, Form
from starlette.responses import JSONResponse
from core.webnetter import Webnetter
from configuration import logger
from basemodels import (
    general_response_model,
    runcommands_request_model,
)

router = APIRouter()


@router.post("/runcommands", response_model=general_response_model)
def run_commands_on_hosts(request: Request, hosts: runcommands_request_model):
    try:
        hosts_dict = hosts.dict()
        webnetter = Webnetter(hosts=hosts_dict["hosts"])
        call = webnetter.runcommand()

        # Put output from all hosts in one string
        output_from_all = ""
        for data in call:
            fixed_data = data["output"].replace(
                "\n", f"\n[{data['host']} {data['software']}] "
            )
            output_from_all += f"[{data['host']} {data['software']}] {fixed_data}\n"

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": call,
                "outputFromAll": output_from_all,
            },
        )

    except Exception as exception:
        logger.warning(f"/webnetter/runcommands:{exception}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "fail",
                "message": "Operation failed, check logging for more information.",
            },
        )


@router.post("/configure", response_model=general_response_model)
async def configure_hosts(
    request: Request, hosts: str = Form(...), config_file: UploadFile = File(...)
):
    try:
        hosts_dict = json.loads(hosts)
        webnetter = Webnetter(hosts=hosts_dict["hosts"])
        call = await webnetter.configure(config_file)

        # Put output from all hosts in one string
        output_from_all = ""
        for data in call:
            fixed_data = data["output"].replace(
                "\n", f"\n[{data['host']} {data['software']}] "
            )
            output_from_all += f"[{data['host']} {data['software']}] {fixed_data}\n"

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": call,
                "outputFromAll": output_from_all,
            },
        )

    except Exception as exception:
        logger.warning(f"/webnetter/configure:{exception}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Operation failed, check logging for more information.",
            },
        )


@router.post("/scp", response_model=general_response_model)
async def scp_file_to_hosts(
    request: Request, hosts: str = Form(...), file: UploadFile = File(...)
):
    try:
        hosts_dict = json.loads(hosts)
        webnetter = Webnetter(hosts=hosts_dict["hosts"])
        call = await webnetter.scp(file)

        # Put output from all hosts in one string
        output_from_all = ""
        for data in call:
            fixed_data = data["output"].replace(
                "\n", f"\n[{data['host']} {data['software']}] "
            )
            output_from_all += f"[{data['host']} {data['software']}] {fixed_data}\n"

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": call,
                "outputFromAll": output_from_all,
            },
        )

    except Exception as exception:
        logger.warning(f"/webnetter/scp:{exception}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "fail",
                "message": "Operation failed, check logging for more information.",
            },
        )
