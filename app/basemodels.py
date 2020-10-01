from pydantic import BaseModel
from typing import List


"""
###################################
########### RUNCOMMANDS ###########
###################################
"""


class response_dict(BaseModel):
    host: str
    up: bool


class model_response_ping(BaseModel):
    status: str
    data: response_dict


"""
###################################
########### RUNCOMMANDS ###########
###################################
"""


class runcommands_request_dict(BaseModel):
    host: str
    username: str
    password: str
    device_type: str
    port: int
    command: str


class model_request_runcommands(BaseModel):
    hosts: List[runcommands_request_dict]


"""
###################################
########### RUNCOMMANDS ###########
###################################
"""

class general_response_dict(BaseModel):
    success: bool
    host: str
    software: str
    output: str


class model_response_general(BaseModel):
    status: str
    data: List[general_response_dict]
    outputFromAll: str
